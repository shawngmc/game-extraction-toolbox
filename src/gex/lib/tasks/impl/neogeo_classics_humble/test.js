
console.log("allocating...");
const buf = Buffer.allocUnsafe(0x80);
buf.fill(0);
buf[0] = 1;
console.log("Initial value: " + buf.toString("hex"));
const tmp = Buffer.allocUnsafe(0x80);
// Process 128 bytes at a time
for (let i = 0; i < buf.length; i += 0x80) {
  tmp.fill(0);
  // For every set of 16 bytes
  for (let y = 0; y < 0x10; y++) {
    let dstData;
    
    // Take the first 4 bytes and space them into a 32 bit array using left shifts
    dstData = buf[i+(y*8)+0] <<  0 |
      buf[i+(y*8)+1] <<  8 |
      buf[i+(y*8)+2] << 16 |
      buf[i+(y*8)+3] << 24;

    // Load the individual bits into the back half of the temp array
    // But how/ what else?
    
    //                        v-----v the spaced-out, copied data
    //                       v--------------------v Get the 
    // tmp[0x43 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
    for (let x = 0; x < 8; x++) {
      tmp[0x43 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
      tmp[0x41 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
      tmp[0x42 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
      tmp[0x40 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
    }
    
    // Take the last 4 bytes and space them into a 32 bit array using left shifts
    dstData = buf[i+(y*8)+4] <<  0 |
      buf[i+(y*8)+5] <<  8 |
      buf[i+(y*8)+6] << 16 |
      buf[i+(y*8)+7] << 24;

    // Load the individual bits into the front half of the temp array
    // But how/what else?
    for (let x = 0; x < 8; x++) {
      tmp[0x03 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
      tmp[0x01 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
      tmp[0x02 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
      tmp[0x00 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
    }
  }

  console.log("Transformed value: " + tmp.toString("hex"));
}