2d转3d过程描述

# 转换2d图片为3d图片PART1 
# 1.把2d图 resize width 
# 2.目前手机为1920*1080 目前测试结果是把size1920*1080 宽度放到1954为最佳3D效果
# 3.把2d图jpg格式转换为png格式
# 4.宽度resize为1/2 ，保存为2d.png


#转换2d图片为3d图片PART2 
# 读取前面的图 png2d
# new 一个 sbsfull ，宽度是png2d的2X
# 左图放偶数列，右图放奇数列
# sbsleft = sbsfull
# sbsright = sbsfull
# 开始在sbsleft和 sbsright 上画mask，调用drawcolumn函数
# mask是3d膜片的斜率
# 打码后保存为sbsleft.png sbsright.png供sbs合并

# 转换2d图片为3d图片PART3 
# 读取 sbsleft.png,sbsright.png
# 调用mergeto3d
# 根据不同distance产生3D图