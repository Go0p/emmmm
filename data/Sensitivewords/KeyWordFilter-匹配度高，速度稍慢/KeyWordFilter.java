package net.jeeshop.web.action.front.modelComment;

import java.io.IOException;
import java.io.InputStream;
import java.util.Enumeration;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 【匹配度可以，速度较慢】
 * Java关键字过滤：http://blog.csdn.net/linfssay/article/details/7599262
 * @author ShengDecheng
 *
 */
public class KeyWordFilter {

	private static Pattern pattern = null;
	private static int keywordsCount = 0;

	// 从words.properties初始化正则表达式字符串
	private static void initPattern() {
		StringBuffer patternBuffer = new StringBuffer();
		try {
			//words.properties
			InputStream in = KeyWordFilter.class.getClassLoader().getResourceAsStream("keywords.properties");
			Properties property = new Properties();
			property.load(in);
			Enumeration<?> enu = property.propertyNames();
			patternBuffer.append("(");
			while (enu.hasMoreElements()) {
				String scontent = (String) enu.nextElement();
				patternBuffer.append(scontent + "|");
				//System.out.println(scontent);
				keywordsCount ++;
			}
			patternBuffer.deleteCharAt(patternBuffer.length() - 1);
			patternBuffer.append(")");
			//System.out.println(patternBuffer);
			// unix换成UTF-8
			// pattern = Pattern.compile(new
			// String(patternBuf.toString().getBytes("ISO-8859-1"), "UTF-8"));
			// win下换成gb2312
			// pattern = Pattern.compile(new String(patternBuf.toString()
			// .getBytes("ISO-8859-1"), "gb2312"));
			// 装换编码
			pattern = Pattern.compile(patternBuffer.toString());
		} catch (IOException ioEx) {
			ioEx.printStackTrace();
		}
	}

	private static String doFilter(String str) {
		Matcher m = pattern.matcher(str);
//		while (m.find()) {// 查找符合pattern的字符串
//			System.out.println("The result is here :" + m.group());
//		}
		// 选择替换方式，这里以* 号代替
		str = m.replaceAll("*");
		return str;
	}

	public static void main(String[] args) {
		long startNumer = System.currentTimeMillis(); 
		initPattern();
		//String str = "我日，艹，fuck，你妹的 干啥呢";
		System.out.println("敏感词的数量：" + keywordsCount);
		String str = "太多的伤yuming感情怀也许只局限于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒哀20于饲养基地 荧幕中的情节，主人公尝试着去用某种方式渐渐的很潇洒地释自杀指南怀那些自己经历的伤感。"  
	            + "然后法轮功 我们的扮演的角色就是跟随着主人yum公的喜红客联盟 怒哀20哀2015/4/16 20152015/4/16乐而过于牵强的把自己的情感也附加于银幕情节中，然后感动就流泪，"  
	            + "关, 人, 流, 电, 发, 情, 太, 限, 法轮功, 个人, 经, 色, 许, 公, 动, 地, 方, 基, 在, 上, 红, 强, 自杀指南, 制, 卡, 三级片, 一, 夜, 多, 手机, 于, 自，"  
	            + "难过就躺在某一个人的怀里尽情的阐述心扉或者手机卡复制器一个人一杯红酒一部电影在夜三级片 深人静的晚上，关上电话静静的发呆着。";  
		System.out.println("被检测字符串长度:"+str.length()); 
		str = doFilter(str);
		//高效Java敏感词、关键词过滤工具包_过滤非法词句：http://blog.csdn.net/ranjio_z/article/details/6299834
		//FilteredResult result = WordFilterUtil.filterText(str, '*');
		long endNumber = System.currentTimeMillis();  
		System.out.println("总共耗时:"+(endNumber-startNumer)+"ms"); 
		System.out.println("替换后的字符串为:\n"+str);
	    //System.out.println("替换后的字符串为:\n"+result.getFilteredContent());
	    //System.out.println("替换后的字符串为1:\n"+result.getOriginalContent());
	    //System.out.println("替换后的字符串为2:\n"+result.getBadWords());
	}
}
