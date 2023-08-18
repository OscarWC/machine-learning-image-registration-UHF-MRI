basePath = "C:/Users/windo/Downloads/head_meshes (1)/2D rot/test/";
for (i = 1; i < 101; i++)
{
	mySavePath = basePath + "00" + i + "_augments.txt";

	c = (7)*random + (-7)*random;

	List.clear();
	List.set("rotation", c)
	m = List.getList;

	File.saveString(m, mySavePath);
	
	mySavePath1 = basePath + "00" + i + "_rt";
	
	open("C:/Users/windo/Downloads/head_meshes (1)/fixed_image0.png");
	
	run("Rotate... ", "angle=c grid=1 interpolation=Bilinear");

	saveAs("PNG", mySavePath1);

	close("\\Others");

	close();
	}