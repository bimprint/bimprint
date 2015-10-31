/**
 * This class is a service class providing methods to generation and conversion between compressed 
 * and uncompressed string representations of GUIDs according to the algorithms used by the 
 * Industry Foundation Classes (IFC). The algorithm is based on an implementation in c as follows: 
 * originally proposed by Jim Forester<br>
 * implemented previously by Jeremy Tammik using hex-encoding<br>
 * Peter Muigg, June 1998<br>
 * Janos Maros, July 2000<br>
 * This class is provided as-is with no warranty.<br>
 * <br>
 * The class GuidCompressor is part of the OPEN IFC JAVA TOOLBOX package. Copyright:
 * CCPL BY-NC-SA 3.0 (cc) 2008 Eike Tauscher, Jan Tulke <br>
 * <br>
 * The OPEN IFC JAVA TOOLBOX package itself (except this class) is licensed under <br>
 * <a rel="license"
 * href="http://creativecommons.org/licenses/by-nc-sa/3.0/de/">Creative Commons
 * Attribution-Non-Commercial- Share Alike 3.0 Germany</a>.<br>
 * Please visit <a
 * href="http://www.openifctools.com">http://www.openifctools.com</a> for more
 * information.<br>
 * 
 * Jan Tulke
 * 1.0 - 24.07.2009
 *
 */
/**
 * This class provides compressing and decompressing GUID's according to algorythm used by Industry Foundation Classes (IFC).
 * It was ported from JAVA.
 * 
 * @author Petrovic Veljko <designlabz@gmail.com>
 * @param {String} string
 */
var GUID = function(string){
	this.Data1 = 0;
	this.Data2 = 0;
	this.Data3 = 0; 
	this.Data4 = [0,0,0,0,0,0,0,0];
	
	if(string != undefined){
		//console.log(string);
		if(string.length == 22)
			this.parseCompressedString(string);
		else
			this.parseUncompressedString(string);
	}
	
};

GUID.prototype.toUncompressedString = function(){

	function pad(string, length){
		while(string.length < length)
			string = "0"+string;
		return string;
	}
	
	str1 = pad(this.Data1.toString(16),8);
	str2 = pad(this.Data2.toString(16),4);
	str3 = pad(this.Data3.toString(16),4);
	var a = this.Data4;
	str4 = 	pad(a[0].toString(16),2) +
			pad(a[1].toString(16),2);
			
	str5 = 	pad(a[2].toString(16),2) +
			pad(a[3].toString(16),2) +
			pad(a[4].toString(16),2) +
			pad(a[5].toString(16),2) +
			pad(a[6].toString(16),2) +
			pad(a[7].toString(16),2);
			
	return str1 + "-" + str2 + "-" + str3 + "-" + str4+ "-" + str5;
	
};

GUID.prototype.parseUncompressedString = function(string){
	var parts = string.split("-");
	
	this.Data1 = parseInt(parts[0], 16);
	this.Data2 = parseInt(parts[1], 16);
	this.Data3 = parseInt(parts[2], 16);
	this.Data4 = [0,0,0,0,0,0,0,0];
		
	var temp = parts[3];
	this.Data4[0] = parseInt(temp.substring(0, 2), 16);
	this.Data4[1] = parseInt(temp.substring(2, 4), 16);
		
	temp = parts[4];
	this.Data4[2] = parseInt(temp.substring(0, 2), 16);
	this.Data4[3] = parseInt(temp.substring(2, 4), 16);
	this.Data4[4] = parseInt(temp.substring(4, 6), 16);
	this.Data4[5] = parseInt(temp.substring(6, 8), 16);
	this.Data4[6] = parseInt(temp.substring(8, 10), 16);
	this.Data4[7] = parseInt(temp.substring(10, 12), 16);
};

GUID.table = [
	'0','1','2','3','4','5','6','7',
	'8','9','A','B','C','D','E','F',
	'G','H','I','J','K','L','M','N',
	'O','P','Q','R','S','T','U','V',
	'W','X','Y','Z','a','b','c','d',
	'e','f','g','h','i','j','k','l',
	'm','n','o','p','q','r','s','t',
	'u','v','w','x','y','z','_','$'
	];
	
GUID.prototype.cvTo64 = function(number, code, len){
	var act, iD, nD, result;
	result = [];
	if (len > 5)
	        return false;
	
	act = number;
	nD = len -1;
	
	for (iD = 0; iD < nD; iD++) {
		var t = Math.floor(act % 64);
		result[nD - iD - 1] = GUID.table[t];
		act /= 64;
	}
	result[len - 1] = '\0';
	        
	
	for(i = 0; i<result.length; i++)
	    	code[i] = result[i];
	 return true;
};

GUID.prototype.cvFrom64 = function(res,str){
	var len, i, j, index;
	
	for(len = 1; len<5; len++)
	    if(str[len]=='\0') break;
	
	res[0]=0;
	
	for (i = 0; i < len; i++) {
        index = -1;
        for (j = 0; j < 64; j++) {
            if (GUID.table[j] == str[i]) {
               index = j;
               break;
            }
        }
        if (index == -1)
            return false;
        
        res[0] = res[0] * 64 + index;
    }
    return true;
};
GUID.prototype.toCompressedString = function(){
	var i,j,n, result;
	result = "";
	var num = [];
	var str = [[],[],[],[],[],[]];
	// Creation of six 32 Bit integers from the components of the GUID structure
	num[0] = (this.Data1 / 0xFFFFFF) & 0xFFFFFF;
	num[1] = this.Data1 & 0xFFFFFF;
	num[2] = this.Data2 * 256 + this.Data3 / 256;
	num[3] = (this.Data3 % 256) * 65536 + this.Data4[0]*256 +this.Data4[1];
	num[4] = this.Data4[2] * 65536 + this.Data4[3] * 256 + this.Data4[4];
	num[5] = this.Data4[5] * 65536 + this.Data4[6] * 256 + this.Data4[7];
	
	
	// Conversion of the numbers into a system using a base of 64
	//
    n = 3;
    for (i = 0; i < 6; i++) {
        if (!this.cvTo64(num[i], str[i], n)) {
            return null;
        }
	    for(j = 0; j<str[i].length; j++)
	    	if(str[i][j]!= '\0') result += str[i][j];
        
        n = 5;
    }
    return result;
};

GUID.prototype.parseCompressedString = function(string){
	var str = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]];
	var len, i,j,k,m;
	var num = [[],[],[],[],[],[]];
	
	len = string.length;
	
	if (len != 22)
	        return false;
	j = 0;
	m = 2;
	      
	for (i = 0; i < 6; i++) {
		for(k = 0; k<m; k++){
	    	str[i][k] = string.charAt(j+k);
	   	}
	    str[i][m]= '\0';
	    j = j + m;
	    m = 4;
	}
	for (i = 0; i < 6; i++) {
		if (!this.cvFrom64(num[i], str[i])) {
	    	return false;
	    }
	}
	
	this.Data1= (num[0][0] * 16777216 + num[1][0]);              // 16-13. bytes
	this.Data2= Math.floor(num[2][0] / 256);                                // 12-11. bytes
	this.Data3= Math.floor((num[2][0] % 256) * 256 + num[3][0] / 65536);    // 10-09. bytes

	this.Data4[0] = Math.floor((num[3][0] / 256) % 256);                   //    08. byte
	this.Data4[1] = Math.floor(num[3][0] % 256);                           //    07. byte

	this.Data4[2] = Math.floor(num[4][0] / 65536);                         //    06. byte
	this.Data4[3] = Math.floor((num[4][0] / 256) % 256);                   //    05. byte
	this.Data4[4] = Math.floor(num[4][0] % 256);                           //    04. byte
	this.Data4[5] = Math.floor(num[5][0] / 65536);                         //    03. byte
	this.Data4[6] = Math.floor((num[5][0] / 256) % 256);                   //    02. byte
	this.Data4[7] = Math.floor(num[5][0] % 256);                           //    01. byte

	return true;

};
