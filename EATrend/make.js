// Tek komut: node make.js <storyId> [--mock]
const { execFileSync } = require('child_process');
const id = process.argv[2], mock = process.argv.includes('--mock');
execFileSync('node', ['voice/tts.js', id, ...(mock ? ['--mock'] : [])], { stdio: 'inherit', cwd: __dirname });
execFileSync('node', ['render/render.js', id], { stdio: 'inherit', cwd: __dirname });
