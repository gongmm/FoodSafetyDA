#/bin/bash
option=$1
case $option in
    ximalaya) python3 爬虫/喜马拉雅爬虫/ximalaya.py #喜马拉雅
    ;;
    shiyaojiandu) python3 爬虫/国家食药监督总局爬虫/shiyaojiandu.py	#食药监督
    ;;
    shipinkeji) python3 爬虫/食品科技网爬虫/shipinkeji.py #食品科技网
    ;;
    shipinanquan) python3 爬虫/中国食品安全网爬虫/shipinanquan.py #中国食品安全网
    ;;
    cctv_food) python3 爬虫/央视网/cctv_food.py #央视网的食品安全相关的新闻
    ;;
    cctv_junk) python3 爬虫/央视网/cctv_junk.py	#央视网其他分类下的新闻
    ;;
    bilibili) python3 爬虫/哔哩哔哩爬虫/bilibili.py	#哔哩哔哩
    ;;
    qingting) python3 爬虫/蜻蜓FM爬虫/qingting.py	#蜻蜓fm
    ;;
    shiantong) python3 爬虫/食安通爬虫/shiantong.py	#食安通爬虫
    ;;
    pearvideo) cd 爬虫/梨视频爬虫/ShipinSpider;scrapy crawl pearvideo_crawler	#梨视频爬虫
    ;;
    image) python3 文本数据提取/动物菜品识别/image.py	#识别图片中的物体
    ;;
    audio) python3 文本数据提取/音频文本提取/audio_process.py	  #提取音频中的文字
    ;;
    movie) python3 文本数据提取/视频文本提取/movie_process.py		#提取视频中文字
    ;;
    text_classification) python3 文本处理/文本分类/text_classification.py		#文本分类进行主题判断
    ;;
    text_cluster) python3 文本处理/文本聚类/text_cluster.py	#文本聚类提取话题
    ;;
    *) echo "Usage: bash $0 [1|2|3]"
        exit 1
    ;;
esac
