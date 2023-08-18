basePath = "C:/Users/windo/Downloads/head_meshes (1)/2D 2 trans/test/";
for (i = 1; i < 101; i++)
{
	mySavePath = basePath + "00" + i + "_augments.txt";
	
	a = (5)*random + (-5)*random;
	b = (5)*random + (-5)*random;

	List.clear();

	List.set("y translation", a)
	List.set("x translation", b)

	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "00" + i + "_rt";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/fixed_image0.png");
	
	run("Translate...", "x=a y=b interpolation=None stack");

	saveAs("PNG", mySavePath1);

	close("\\Others");

	close();
	}