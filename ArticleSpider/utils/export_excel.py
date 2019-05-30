"""
    create by Gray 2019-05-27
"""
import xlwt
import json


class JobboleExportExcel:
    # 导出json数据到Excel表
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('jobbole_article')
    head = ['标题', '链接', '标签', '点赞', '收藏', '评论']  # 表头
    for h in range(len(head)):
        sheet.write(0, h, head[h])  # 写入表头

    @classmethod
    def export(cls):
        with open('articleExport.json', encoding='utf-8') as f:
            temp = json.loads(f.read())
            temp = sorted(temp, key=cls.sort, reverse=True)
            i = 1
            for obj in temp:
                cls.sheet.write(i, 0, obj['title'])
                cls.sheet.write(i, 1, obj['url'])
                cls.sheet.write(i, 2, obj['tags'])
                cls.sheet.write(i, 3, obj.get('praise_num', 0))
                cls.sheet.write(i, 4, obj.get('collect_num', 0))
                cls.sheet.write(i, 5, obj.get('comment_num', 0))
                i += 1
            cls.book.save('/Users/gulei/Desktop/jobbole_article.xls')

    @classmethod
    def sort(cls, article):
        return article.get('collect_num', 0)
