const fs = require('fs');

const base = 'd:/Buaa_2026/AI-Learning-Route/\u8bb2\u4e49/\u7b2c1\u5468/Prompt-Engineering';
const imgDir = base + '/images';
const mapFile = base + '/figure-map.txt';

let changed = false;
if (fs.existsSync(imgDir)) {
  fs.rmSync(imgDir, { recursive: true, force: true });
  console.log('removed images dir:', !fs.existsSync(imgDir));
  changed = true;
} else {
  console.log('images dir already absent');
}
if (fs.existsSync(mapFile)) {
  fs.unlinkSync(mapFile);
  console.log('removed figure-map.txt:', !fs.existsSync(mapFile));
  changed = true;
} else {
  console.log('figure-map.txt already absent');
}
console.log('cleanup done:', changed);
