import * as vscode from "vscode";

// Define the response type
interface CommandResponse {
  status: string;
  action: string;
  text: string;
  line?: number;
  line_end?: number;
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
  } else {
    statusBarItem.text = "$(mic) Voice Mode";
    statusBarItem.backgroundColor = undefined;
  }
  statusBarItem.show(); // always visible
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
    } else if (data.action === "remove_line") {
      await handleRemoveLine(editor, data.line);
    } else if (data.action === "select_lines") {
      await handleSelectLines(editor, data.line, data.line_end);
    } else if (data.action === "remove_lines") {
      await handleRemoveLines(editor, data.line, data.line_end);
    } else if (data.action === "run_code") {
      await vscode.commands.executeCommand("workbench.action.debug.run");
      vscode.window.setStatusBarMessage("Running code...", 3000);
    } else if (data.action === "undo") {
      await vscode.commands.executeCommand("undo");
      vscode.window.setStatusBarMessage("Undid last action", 2000);
    } else if (data.action === "redo") {
      await vscode.commands.executeCommand("redo");
      vscode.window.setStatusBarMessage("Redid last action", 2000);
    } else if (data.action === "comment_line") {
      await vscode.commands.executeCommand("editor.action.addCommentLine");
    } else if (data.action === "uncomment_line") {
      await vscode.commands.executeCommand("editor.action.removeCommentLine");
    } else if (data.action === "toggle_comment") {
      await vscode.commands.executeCommand("editor.action.commentLine");
    } else if (data.action === "goto_top") {
      await vscode.commands.executeCommand("cursorTop");
    } else if (data.action === "goto_bottom") {
      await vscode.commands.executeCommand("cursorBottom");
    } else if (data.action === "duplicate_line") {
      await vscode.commands.executeCommand("editor.action.copyLinesDownAction");
    } else if (data.action === "stop_listening") {
      isListening = false;
      updateStatusBar(false);
      vscode.window.showInformationMessage("Voice Loop Stopped");
    } else if (data.action === "goto_definition" && data.name) {
      await vscode.commands.executeCommand("workbench.action.quickOpen", "@" + data.name);
    } else if (data.action === "create_file" && data.name) {
      await handleCreateFile(data.name);
    } else if (data.action === "open_file" && data.name) {
      await handleOpenFile(data.name);
    } else if (data.action === "save_file") {
      await editor.document.save();
      vscode.window.setStatusBarMessage("File saved", 2000);
    } else if (data.action === "close_file") {
      await vscode.commands.executeCommand("workbench.action.closeActiveEditor");
    } else if (data.action === "select_all") {
      await vscode.commands.executeCommand("editor.action.selectAll");
    } else if (data.action === "copy") {
      await vscode.commands.executeCommand("editor.action.clipboardCopyAction");
      vscode.window.setStatusBarMessage("Copied to clipboard", 2000);
    } else if (data.action === "cut") {
      await vscode.commands.executeCommand("editor.action.clipboardCutAction");
      vscode.window.setStatusBarMessage("Cut to clipboard", 2000);
    } else if (data.action === "paste") {
      await vscode.commands.executeCommand("editor.action.clipboardPasteAction");
    } else if (data.action === "find") {
      await vscode.commands.executeCommand("actions.find");
    } else if (data.action === "replace") {
      await vscode.commands.executeCommand("editor.action.startFindReplaceAction");
    } else if (data.action === "new_line_above") {
      await vscode.commands.executeCommand("editor.action.insertLineAbove");
    } else if (data.action === "new_line_below") {
      await vscode.commands.executeCommand("editor.action.insertLineAfter");
    } else if (data.action === "delete_word") {
      await vscode.commands.executeCommand("deleteWordRight"); // Or deleteWordLeft
    } else if (data.action === "select_word") {
      await vscode.commands.executeCommand("editor.action.selectWord");
    } else if (data.action === "select_line") {
      await vscode.commands.executeCommand("editor.action.selectLine");
    } else if (data.action === "go_to_start_of_line") {
      await vscode.commands.executeCommand("cursorHome");
    } else if (data.action === "go_to_end_of_line") {
      await vscode.commands.executeCommand("cursorEnd");
    } else {
      console.warn("Unhandled action:", data.action);
      if (!isListening) {
        vscode.window.showWarningMessage(`Unhandled voice command action: ${data.action}`);
      }
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

async function handleSelectLines(
  editor: vscode.TextEditor,
  startLine: number | undefined,
  endLine: number | undefined,
) {
  if (startLine === undefined || endLine === undefined) return;

  const document = editor.document;
  const startIdx = Math.max(0, startLine - 1);
  const endIdx = Math.min(document.lineCount - 1, Math.max(0, endLine - 1));

  if (startIdx < document.lineCount) {
    const startPos = new vscode.Position(startIdx, 0);
    const endPos = new vscode.Position(
      endIdx,
      document.lineAt(endIdx).text.length,
    );
    editor.selection = new vscode.Selection(startPos, endPos);
    editor.revealRange(new vscode.Range(startPos, endPos));
  }
}

async function handleRemoveLines(
  editor: vscode.TextEditor,
  startLine: number | undefined,
  endLine: number | undefined,
) {
  if (startLine === undefined || endLine === undefined) return;

  const document = editor.document;
  const startIdx = Math.max(0, startLine - 1);
  const endIdx = Math.max(0, endLine - 1);

  if (startIdx < document.lineCount) {
    const startPos = new vscode.Position(startIdx, 0);
    let endPos;

    if (endIdx + 1 < document.lineCount) {
      endPos = new vscode.Position(endIdx + 1, 0);
    } else {
      endPos = new vscode.Position(
        Math.min(endIdx, document.lineCount - 1),
        document.lineAt(Math.min(endIdx, document.lineCount - 1)).text.length,
      );
    }

    const range = new vscode.Range(startPos, endPos);
    await editor.edit((editBuilder) => {
      editBuilder.delete(range);
    });
    vscode.window.setStatusBarMessage(
      `Removed lines ${startLine} to ${endLine}`,
      3000,
    );
  }
}

async function handleCreateFile(name: string) {
  const workspaceFolders = vscode.workspace.workspaceFolders;
  if (!workspaceFolders) {
    vscode.window.showErrorMessage("No workspace folder open");
    return;
  }

  const newFileUri = vscode.Uri.joinPath(workspaceFolders[0].uri, name);
  try {
    // Create an empty file
    await vscode.workspace.fs.writeFile(newFileUri, new Uint8Array());
    // Open it
    const document = await vscode.workspace.openTextDocument(newFileUri);
    await vscode.window.showTextDocument(document);
    vscode.window.showInformationMessage(`Created and opened ${name}`);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Failed to create file: ${err.message}`);
  }
}

async function handleOpenFile(name: string) {
  const files = await vscode.workspace.findFiles(`**/${name}`, null, 1);
  if (files.length > 0) {
    const document = await vscode.workspace.openTextDocument(files[0]);
    await vscode.window.showTextDocument(document);
  } else {
    // Try quick open if not found directly
    await vscode.commands.executeCommand("workbench.action.quickOpen", name);
  }
}

export function deactivate() {}
