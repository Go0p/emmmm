
public static void main(String[] args) {
		long startNumer = System.currentTimeMillis(); 
		System.out.println("敏感词的数量：" + keywordsCount);
		String str = "太多的伤yuming感情怀也许只局限于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒哀20于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒哀20哀2015/4/16 20152015/4/16乐而过于牵强的把自己的情感也附加于银幕情节中，然后感动就流泪，"  
	            + "关, 人, 流, 电, 发, 情, 太, 限, 法轮功, 个人, 经, 色, 许, 公, 动, 地, 方, 基, 在, 上, 红, 强, 自杀指南, 制, 卡, 三级片, 一, 夜, 多, 手机, 于, 自，"  
	            + "难过就躺在某一个人的怀里尽情的阐述心扉或者手机卡复制器一个人一杯红酒一部电影在夜三级片 深人静的晚上，关上电话静静的发呆着。";  
		System.out.println("被检测字符串长度:"+str.length()); 
		//高效Java敏感词、关键词过滤工具包_过滤非法词句：http://blog.csdn.net/ranjio_z/article/details/6299834
		FilteredResult result = WordFilterUtil.filterText(str, '*');
		long endNumber = System.currentTimeMillis();  
		System.out.println("总共耗时:"+(endNumber-startNumer)+"ms"); 
	    System.out.println("替换后的字符串为:\n"+result.getFilteredContent());
	    System.out.println("替换后的字符串为1:\n"+result.getOriginalContent());
	    System.out.println("替换后的字符串为2:\n"+result.getBadWords());
	}