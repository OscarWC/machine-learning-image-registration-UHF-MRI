basePath = "C:/Users/windo/Downloads/head_meshes (1)/2D 1 trans/";
for (i = 1; i < 1001; i++)
{
	mySavePath = basePath + "00" + i + "_augments.txt";
	
	a = (7)*random + (-7)*random;

	List.clear();

	List.set("y translation", a)

	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "00" + i + "_rt";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/fixed_image0.png");
	
	run("Translate...", "x=a y=0 interpolation=None stack");

	saveAs("PNG", mySavePath1);

	close("\\Others");

	close();
	}