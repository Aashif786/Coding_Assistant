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
    const disposable = vscode.commands.registerCommand('voice-to-code.insertText', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        const contextPayload = {
            language: editor.document.languageId,
            cursorLine: editor.selection.active.line,
            hasSelection: !editor.selection.isEmpty
        };
        try {
            // ⏱ Timeout protection
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            const response = await fetch('http://127.0.0.1:8000/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(contextPayload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error('Backend error');
            }
            const data = await response.json();
            // 🔒 Strict validation
            if (!data ||
                data.status !== 'ok' ||
                typeof data.text !== 'string') {
                vscode.window.showErrorMessage('Invalid backend response');
                return;
            }
            await editor.edit(editBuilder => {
                editBuilder.insert(editor.selection.active, `\n${data.text}\n`);
            });
            if (!data.text.trim()) {
                vscode.window.showWarningMessage('No voice command detected');
                return;
            }
            if (data.action === 'insert') {
                vscode.window.setStatusBarMessage('Voice command executed successfully', 3000);
            }
            if (data.action === 'message') {
                vscode.window.showInformationMessage(data.text);
            }
        }
        catch (error) {
            if (error.name === 'AbortError') {
                vscode.window.showErrorMessage('Voice service unavailable. Please try again.');
            }
            else {
                vscode.window.showErrorMessage('Voice service unavailable. Please try again.');
            }
        }
    });
    context.subscriptions.push(disposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map