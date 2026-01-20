import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

	const disposable = vscode.commands.registerCommand(
		'voice-to-code.insertText',
		async () => {

			const editor = vscode.window.activeTextEditor;
			if (!editor) {return;}

			const contextPayload = {
			language: editor.document.languageId,
			cursorLine: editor.selection.active.line,
			hasSelection: !editor.selection.isEmpty
			};

			try {
				// ⏱ Timeout protection
				const controller = new AbortController();
				const timeoutId = setTimeout(() => controller.abort(), 10000);

				const response = await fetch(
				'http://127.0.0.1:8000/command',{
					method: 'POST',
					headers: {'Content-Type': 'application/json'},
					body: JSON.stringify(contextPayload),
					signal: controller.signal
				});

				clearTimeout(timeoutId);

				if (!response.ok) {
					throw new Error('Backend error');
				}

				const data: any = await response.json();

				// 🔒 Strict validation
				if (
					!data ||
					data.status !== 'ok' ||
					typeof data.text !== 'string'
				) {
					vscode.window.showErrorMessage('Invalid backend response');
					return;
				}

				await editor.edit(editBuilder => {
					editBuilder.insert(
						editor.selection.active,
						`\n${data.text}\n`
					);
				});
				
				if (!data.text.trim()) {
					vscode.window.showWarningMessage(
						'No voice command detected'
					);
					return;
				}

				if (data.action === 'insert') {
					vscode.window.setStatusBarMessage(
						'Voice command executed successfully',
						3000
					);
				}

				if (data.action === 'message') {
					vscode.window.showInformationMessage(data.text);
				}


			} catch (error: any) {

				if (error.name === 'AbortError') {
					vscode.window.showErrorMessage(
						'Voice service unavailable. Please try again.'
					);
				} else {
					vscode.window.showErrorMessage(
						'Voice service unavailable. Please try again.'
					);
				}
			}
		}
	);

	context.subscriptions.push(disposable);
}

export function deactivate() {}
