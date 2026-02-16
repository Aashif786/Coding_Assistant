import * as vscode from "vscode";

// Define the response type
interface CommandResponse {
  status: string;
  action: string;
  text: string;
  line?: number;
  intent?: any;
  name?: string;
}

let isListening = false;
let statusBarItem: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
  console.log("Voice to Code extension activated");

  // Create status bar item
  statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100,
  );
  statusBarItem.command = "voice-to-code.insertLoop";
  context.subscriptions.push(statusBarItem);

  // Main single-shot command
  const insertTextDisposable = vscode.commands.registerCommand(
    "voice-to-code.insertText",
    async () => {
      await processVoiceCommand();
    },
  );

  // Continuous loop command
  const insertLoopDisposable = vscode.commands.registerCommand(
    "voice-to-code.insertLoop",
    async () => {
      if (isListening) {
        isListening = false;
        updateStatusBar(false);
        vscode.window.showInformationMessage("Voice Loop Stopped");
        return;
      }

      isListening = true;
      updateStatusBar(true);
      vscode.window.showInformationMessage("Voice Loop Started");

      while (isListening) {
        try {
          await processVoiceCommand();
          // Small delay to prevent tight loop if backend returns immediately
          await new Promise((resolve) => setTimeout(resolve, 100));
        } catch (e) {
          console.error("Loop error:", e);
          // Don't crash the loop on error, just wait a bit and retry
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }
      }
      updateStatusBar(false);
    },
  );

  // Test command for debug_goto endpoint
  const testDisposable = vscode.commands.registerCommand(
    "voice-to-code.testGoto",
    async () => {
      // ... existing test logic ...
    },
  );

  // Simulation command
  const simulateDisposable = vscode.commands.registerCommand(
    "voice-to-code.simulateCommand",
    async () => {
      const text = await vscode.window.showInputBox({
        prompt: 'Enter command to simulate (e.g. "comment", "run code")',
        placeHolder: "command text...",
      });
      if (text) {
        await processVoiceCommand(text);
      }
    },
  );

  // Add commands to subscriptions
  context.subscriptions.push(
    insertTextDisposable,
    insertLoopDisposable,
    testDisposable,
    simulateDisposable,
  );

  // Log registered commands
  vscode.commands.getCommands().then((commands) => {
    const myCommands = commands.filter((cmd) => cmd.includes("voice-to-code"));
    console.log("📋 Registered voice-to-code commands:", myCommands);
  });
}

function updateStatusBar(active: boolean) {
  if (active) {
    statusBarItem.text = "$(mic) Listening...";
    statusBarItem.backgroundColor = new vscode.ThemeColor(
      "statusBarItem.warningBackground",
    );
    statusBarItem.show();
  } else {
    statusBarItem.text = "$(mic) Voice Mode";
    statusBarItem.backgroundColor = undefined;
    statusBarItem.hide(); // Or show as idle
  }
}

async function processVoiceCommand(mockText?: string) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    // If no editor is active, we can't do much.
    // In loop mode, we might just wait.
    if (!isListening && !mockText) {
      vscode.window.showWarningMessage("No active editor");
    }
    return;
  }

  const contextPayload = {
    language: editor.document.languageId,
    cursorLine: editor.selection.active.line,
    hasSelection: !editor.selection.isEmpty,
    totalLines: editor.document.lineCount,
    mock_text: mockText || null,
  };

  try {
    // ⏱ Timeout protection
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 12000); // Increased timeout for loop buffer

    console.log("📡 Calling backend...");
    const response = await fetch("http://127.0.0.1:8000/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contextPayload),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = (await response.json()) as CommandResponse;
    console.log("📦 Backend response:", data);

    // 🔒 Strict validation
    if (!data || data.status !== "ok") {
      return;
    }

    // Handle move_cursor action
    if (data.action === "move_cursor") {
      await handleMoveCursor(editor, data.line || 1);
      return;
    }

    // Handle insert action
    if (data.action === "insert") {
      await handleInsert(editor, data.text);
      return;
    }

    // Handle message action
    if (data.action === "message") {
      if (
        typeof data.text === "string" &&
        data.text !== "No voice command detected"
      ) {
        // Only show interesting messages, skip "silence" messages in loop
        vscode.window.showInformationMessage(data.text);
      }
      return;
    }

    // remove line
    if (data.action === "remove_line") {
      await handleRemoveLine(editor, data.line);
      return;
    }

    if (data.action === "run_code") {
      await vscode.commands.executeCommand("workbench.action.debug.run");
      // Or 'workbench.action.terminal.runActiveFile' or 'python.execInTerminal'
      vscode.window.setStatusBarMessage("Running code...", 3000);
      return;
    }

    if (data.action === "undo") {
      await vscode.commands.executeCommand("undo");
      vscode.window.setStatusBarMessage("Undid last action", 2000);
      return;
    }

    if (data.action === "redo") {
      await vscode.commands.executeCommand("redo");
      vscode.window.setStatusBarMessage("Redid last action", 2000);
      return;
    }

    if (data.action === "comment_line") {
      await vscode.commands.executeCommand("editor.action.addCommentLine");
      return;
    }

    if (data.action === "uncomment_line") {
      await vscode.commands.executeCommand("editor.action.removeCommentLine");
      return;
    }

    if (data.action === "goto_top") {
      await vscode.commands.executeCommand("cursorTop");
      await vscode.commands.executeCommand("cursorTop"); // Ensure scroll to top
      return;
    }

    if (data.action === "goto_bottom") {
      await vscode.commands.executeCommand("cursorBottom");
      await vscode.commands.executeCommand("cursorBottom"); // Ensure scroll to bottom
      return;
    }

    if (data.action === "duplicate_line") {
      await vscode.commands.executeCommand("editor.action.copyLinesDownAction");
      return;
    }

    if (data.action === "stop_listening") {
      isListening = false;
      updateStatusBar(false);
      vscode.window.showInformationMessage("Voice Loop Stopped");
      return;
    }

    if (data.action === "goto_definition" && data.name) {
      // Use Quick Open to search for the symbol in the current file
      await vscode.commands.executeCommand(
        "workbench.action.quickOpen",
        "@" + data.name,
      );
      return;
    }
  } catch (error: any) {
    console.error("❌ Error:", error);

    if (error.name === "AbortError") {
      // Timeout is expected if we are just listening in a loop.
      // Don't show error message in loop mode typically, unless debugging.
      if (!isListening) {
        vscode.window.showErrorMessage(
          "Voice service timeout. Please try again.",
        );
      }
    } else {
      if (!isListening) {
        vscode.window.showErrorMessage(`Voice service error: ${error.message}`);
      }
    }
  }
}

async function handleMoveCursor(
  editor: vscode.TextEditor,
  targetLineOneBased: number,
) {
  const targetLineZeroBased = Math.max(0, targetLineOneBased - 1);
  const document = editor.document;
  const currentLines = document.lineCount;

  console.log(
    `📊 Moving to line ${targetLineOneBased} (0-based: ${targetLineZeroBased})`,
  );

  // If target line doesn't exist, add required newlines
  if (targetLineZeroBased >= currentLines) {
    const linesToAdd = targetLineZeroBased - currentLines + 1;
    await editor.edit((editBuilder) => {
      const lastLine = document.lineAt(currentLines - 1);
      const newLines = "\n".repeat(linesToAdd);
      editBuilder.insert(lastLine.range.end, newLines);
    });
  }

  // Create position and move cursor
  const position = new vscode.Position(targetLineZeroBased, 0);
  editor.selection = new vscode.Selection(position, position);

  // Reveal in view
  editor.revealRange(
    new vscode.Range(position, position),
    vscode.TextEditorRevealType.InCenter,
  );

  console.log(`✅ Cursor moved to line ${targetLineOneBased}`);
  // In loop mode, repeated messages might be annoying, maybe status bar flash?
  if (!isListening) {
    vscode.window.showInformationMessage(
      `Cursor moved to line ${targetLineOneBased}`,
    );
  }
}

async function handleInsert(editor: vscode.TextEditor, text: string) {
  if (typeof text !== "string" || !text.trim()) {
    return;
  }

  await editor.edit((editBuilder) => {
    editBuilder.insert(editor.selection.active, `\n${text}\n`);
  });

  vscode.window.setStatusBarMessage("Code inserted successfully", 3000);
}

async function handleRemoveLine(
  editor: vscode.TextEditor,
  line: number | undefined,
) {
  const document = editor.document;

  // Step 1: Navigate if line number exists and is different from current
  if (typeof line === "number") {
    const targetLine = line - 1;
    if (targetLine >= document.lineCount) {
      // Can't remove a line that doesn't exist.
      return;
    }
    const position = new vscode.Position(targetLine, 0);
    editor.selection = new vscode.Selection(position, position);
  }

  // Step 2: Remove the line at cursor
  const currentLine = editor.selection.active.line;

  if (currentLine < document.lineCount) {
    const range = document.lineAt(currentLine).rangeIncludingLineBreak;
    await editor.edit((editBuilder) => {
      editBuilder.delete(range);
    });
    vscode.window.setStatusBarMessage(`Removed line ${currentLine + 1}`, 3000);
  }
}

export function deactivate() {}
