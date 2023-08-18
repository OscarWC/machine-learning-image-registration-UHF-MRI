basePath = "C:/Users/windo/PycharmProjects/MLReg/";
for (i = 1; i < 11; i++)
{
	mySavePath = basePath + "00" + i + "_augments.txt";
	
	a = (7)*random + (-7)*random;

	List.clear();

	List.set("y translation", a)

	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "00" + i + "_rt";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/headmeshdilatedscaled1.1.tif");
	
	run("Translate...", "x=a y=0 interpolation=None stack");

	saveAs("Tiff", mySavePath1);

	close("\\Others");

	close();
	}