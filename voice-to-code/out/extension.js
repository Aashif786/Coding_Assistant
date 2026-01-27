"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
function activate(context) {
    console.log('Voice to Code extension activated');
    // Main voice command
    const disposable = vscode.commands.registerCommand('voice-to-code.insertText', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor');
            return;
        }
        const contextPayload = {
            language: editor.document.languageId,
            cursorLine: editor.selection.active.line,
            hasSelection: !editor.selection.isEmpty,
            totalLines: editor.document.lineCount // Added for backend awareness
        };
        try {
            // ⏱ Timeout protection
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            console.log('📡 Calling backend...');
            const response = await fetch('http://127.0.0.1:8000/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(contextPayload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }
            const data = await response.json();
            console.log('📦 Backend response:', data);
            // 🔒 Strict validation
            if (!data || data.status !== 'ok') {
                vscode.window.showErrorMessage('Invalid backend response');
                return;
            }
            // Handle move_cursor action
            if (data.action === 'move_cursor') {
                const editor = vscode.window.activeTextEditor;
                if (!editor) {
                    vscode.window.showErrorMessage('No active editor');
                    return;
                }
                // Get target line (1-based from backend)
                const targetLineOneBased = data.line || 1;
                const targetLineZeroBased = Math.max(0, targetLineOneBased - 1);
                const document = editor.document;
                const currentLines = document.lineCount;
                console.log(`📊 Moving to line ${targetLineOneBased} (0-based: ${targetLineZeroBased})`);
                console.log(`📄 Document has ${currentLines} lines`);
                // If target line doesn't exist, add required newlines
                if (targetLineZeroBased >= currentLines) {
                    const linesToAdd = targetLineZeroBased - currentLines + 1;
                    console.log(`➕ Need to add ${linesToAdd} new lines`);
                    await editor.edit(editBuilder => {
                        const lastLine = document.lineAt(currentLines - 1);
                        const newLines = '\n'.repeat(linesToAdd);
                        editBuilder.insert(lastLine.range.end, newLines);
                    });
                    console.log(`✅ Added ${linesToAdd} new lines`);
                }
                // Create position and move cursor
                const position = new vscode.Position(targetLineZeroBased, 0);
                // Set selection
                editor.selection = new vscode.Selection(position, position);
                // Reveal in view
                editor.revealRange(new vscode.Range(position, position), vscode.TextEditorRevealType.InCenter);
                console.log(`✅ Cursor moved to line ${targetLineOneBased}`);
                vscode.window.showInformationMessage(`Cursor moved to line ${targetLineOneBased}`);
                return;
            }
            // Handle insert action
            if (data.action === 'insert') {
                if (typeof data.text !== 'string') {
                    vscode.window.showErrorMessage('Invalid text in response');
                    return;
                }
                if (!data.text.trim()) {
                    vscode.window.showWarningMessage('No code to insert');
                    return;
                }
                await editor.edit(editBuilder => {
                    editBuilder.insert(editor.selection.active, `\n${data.text}\n`);
                });
                vscode.window.setStatusBarMessage('Code inserted successfully', 3000);
                return;
            }
            // Handle message action
            if (data.action === 'message') {
                if (typeof data.text === 'string') {
                    vscode.window.showInformationMessage(data.text);
                }
                return;
            }
            // Unknown action
            vscode.window.showWarningMessage(`Unknown action: ${data.action}`);
        }
        catch (error) {
            console.error('❌ Error:', error);
            if (error.name === 'AbortError') {
                vscode.window.showErrorMessage('Voice service timeout. Please try again.');
            }
            else {
                vscode.window.showErrorMessage(`Voice service error: ${error.message}`);
            }
        }
    });
    // Test command for debug_goto endpoint
    const testDisposable = vscode.commands.registerCommand('voice-to-code.testGoto', async () => {
        try {
            console.log('🧪 Testing debug_goto endpoint...');
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage('No active editor');
                return;
            }
            // Request line 30 for testing
            const response = await fetch('http://127.0.0.1:8000/debug_goto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ line: 30 }) // Test with line 30
            });
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API error:', response.status, errorText);
                vscode.window.showErrorMessage(`API error: ${response.status}`);
                return;
            }
            const data = await response.json();
            console.log('✅ Debug response:', data);
            if (data.action === 'move_cursor' && data.line !== undefined) {
                const targetLineOneBased = data.line;
                const targetLineZeroBased = Math.max(0, targetLineOneBased - 1);
                const document = editor.document;
                const currentLines = document.lineCount;
                // Add lines if needed
                if (targetLineZeroBased >= currentLines) {
                    const linesToAdd = targetLineZeroBased - currentLines + 1;
                    await editor.edit(editBuilder => {
                        const lastLine = document.lineAt(currentLines - 1);
                        const newLines = '\n'.repeat(linesToAdd);
                        editBuilder.insert(lastLine.range.end, newLines);
                    });
                }
                // Move cursor
                const position = new vscode.Position(targetLineZeroBased, 0);
                editor.selection = new vscode.Selection(position, position);
                editor.revealRange(new vscode.Range(position, position), vscode.TextEditorRevealType.InCenter);
                vscode.window.showInformationMessage(`Test: Moved to line ${targetLineOneBased}`);
            }
        }
        catch (error) {
            console.error('❌ Test failed:', error);
            vscode.window.showErrorMessage(`Test failed: ${error.message}`);
        }
    });
    // Add both commands to subscriptions
    context.subscriptions.push(disposable, testDisposable);
    // Log registered commands
    vscode.commands.getCommands().then(commands => {
        const myCommands = commands.filter(cmd => cmd.includes('voice-to-code'));
        console.log('📋 Registered voice-to-code commands:', myCommands);
    });
}
function deactivate() { }
//# sourceMappingURL=extension.js.map