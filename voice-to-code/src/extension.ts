import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

	const disposable = vscode.commands.registerCommand(
		'voice-to-code.insertText',
		async () => {

			const editor = vscode.window.activeTextEditor;
			if (!editor) {
				vscode.window.showErrorMessage('No active editor found');
				return;
			}

			try {
				// ⏱ Timeout protection
				const controller = new AbortController();
				const timeoutId = setTimeout(() => controller.abort(), 3000);

				const response = await fetch(
					'http://127.0.0.1:8000/command',
					{ signal: controller.signal }
				);

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

			} catch (error: any) {

				if (error.name === 'AbortError') {
					vscode.window.showErrorMessage(
						'Backend timeout (not responding)'
					);
				} else {
					vscode.window.showErrorMessage(
						'Backend not reachable'
					);
				}
			}
		}
	);

	context.subscriptions.push(disposable);
}

export function deactivate() {}
