basePath = "C:/Users/windo/PycharmProjects/Registration1/";
basePath2 = "C:/Users/windo/Downloads/head_meshes (1)/GRAPPA/";
for (i = 1; i < 101; i++)
{
	mySavePath = basePath + "folder2/" + "00" + i + "_augments.txt";
	mySavePath0 = basePath + "groundtruths/" + "00" + i + "_augments.txt";
	
	a = (7)*random + (-7)*random;
	b = (5)*random + (-5)*random;
	c = (5)*random + (-5)*random;
	d = (7)*random + (-7)*random;
	e = (5)*random + (-5)*random;
	f = (5)*random + (-5)*random;
	g = (7)*random + (-7)*random;
	h = (5)*random + (-5)*random;
	j = (5)*random + (-5)*random;

	List.clear();

	List.set("z rotation", g)
	List.set("z translation", c + h)
	List.set("y rotation", a)
	List.set("y translation", b + e)
	List.set("x rotation", -d)
	List.set("x translation", f + j)

	m = List.getList;

	File.saveString(m, mySavePath);
	File.saveString(m, mySavePath0);
	
	mySavePath1 = basePath2 + "00" + i + "_rt_n";
	mySavePath2 = basePath2 + "00" + i + "_rt_d";
	mySavePath3 = basePath2 + "00" + i + "_rt_u";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/headmeshdilatedscaled1.2.tif");

	run("Reslice [/]...", "output=1000.000 start=Left avoid");
	run("Rotate... ", "angle=a grid=1 interpolation=Bilinear stack");
	run("Translate...", "x=j y=c interpolation=None stack");
	run("Reslice [/]...", "output=1000.000 start=Top rotate avoid");
	
	run("Reslice [/]...", "output=1000.000 start=Top avoid");
	run("Rotate... ", "angle=d grid=1 interpolation=Bilinear stack");
	run("Translate...", "x=e y=h interpolation=None stack");
	run("Reslice [/]...", "output=1000.000 start=Top avoid");
	
	run("Rotate... ", "angle=g grid=1 interpolation=Bilinear stack");
	run("Translate...", "x=b y=f interpolation=None stack");

	saveAs("Tiff", mySavePath1);
	saveAs("Tiff", mySavePath2);
	saveAs("Tiff", mySavePath3);

	close("\\Others");
	
//	mySavePath2 = basePath + "noisydata/" + "00" + i + "_rtn";
	
//	run("Add Specified Noise...", "stack standard=10");

//	saveAs("Tiff", mySavePath2);

	close();
	}