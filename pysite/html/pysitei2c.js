// Example pysitei2c.js - micropython-webserver - free sotware under GNU GPL
// Author: (c)2022 Tóthpál István <istvan@tothpal.eu>

function filldata(){
  if (I2Cscan!==false) {
    resdiv = document.getElementById("scan");
    resdiv.innerHTML = "<p>Scan Result: </p><p>";
    if (I2Cscan.length==0) {
      resdiv.innerHTML += "No device found</p>";
    }
    else {
      i=0;
      while (i<I2Cscan.length-1) {
        resdiv.innerHTML += "0x"+("0"+I2Cscan[i++].toString(16)).substr(-2)+", ";
      }
      resdiv.innerHTML += "0x"+("0"+I2Cscan[i++].toString(16)).substr(-2) + "<p>";
    
      resdiv = document.getElementById("dump");
      l = document.createElement('label');
      l.innerHTML="Select device (address): ";
      l.htmlFor="addr";
      resdiv.append(l);
      s = document.createElement('select');
      s.id="addr";
      s.name="addr";
      i=0;
      while (i<I2Cscan.length) {
        o = document.createElement('option');
        o.value = I2Cscan[i];
        if (I2Cscan[i]==addr) {
          o.selected=true;
        }
        o.text = "0x"+("0"+I2Cscan[i++].toString(16)).substr(-2);
        s.append(o);
      }
      resdiv.append(s);   
      i = document.createElement('input');
      i.name="I2C";
      i.type="submit";
      i.value="Dump";
      i.style="margin-left:10px;"
      resdiv.append(i);
    }
  }
}

window.onload=filldata
