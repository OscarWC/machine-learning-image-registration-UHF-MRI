basePath = "C:/Users/windo/Downloads/head_meshes (1)/2D 2 transrot/";
for (i = 1; i < 10001; i++)
{
	mySavePath = basePath + "00" + i + "_augments.txt";
	
	a = (5)*random + (-5)*random;
	b = (5)*random + (-5)*random;
	c = (7)*random + (-7)*random;

	List.clear();

	List.set("y translation", a)
	List.set("x translation", b)
	List.set("rotation", c)

	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "00" + i + "_rt";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/fixed_image0.png");
	
	run("Rotate... ", "angle=c grid=1 interpolation=Bilinear");
	run("Translate...", "x=a y=b interpolation=None stack");

	saveAs("PNG", mySavePath1);

	close("\\Others");

	close();
	}