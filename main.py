import uvicorn
from fastapi import FastAPI
from elasticdao import elastic_dao
import xlsxwriter
import datetime
from starlette.responses import FileResponse
import pathlib

app = FastAPI()


@app.get("/generateinfluencer")
def generate_influencer(influencer: str, start: str, end: str):
    file_location = str(pathlib.Path(__file__).parent.absolute()) + '/'
    string_start = datetime.datetime.strptime(start, '%Y%m%d').strftime('%d %B %Y')
    string_end = datetime.datetime.strptime(end, '%Y%m%d').strftime('%d %B %Y')
    file_name = 'report_influencer_' + str(influencer).replace(' ', '_') + '_' + string_start.replace(' ','_') + '_until_' + string_end.replace(' ', '_') + '.xlsx'
    date_title = string_start + ' until ' + string_end
    data_list, num = elastic_dao.get_data_elastic(influencer=influencer, start=start, end=end)

    workbook = xlsxwriter.Workbook(file_location + str(file_name))
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 27)
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(2, 2, 27)
    worksheet.set_column(3, 3, 39)
    worksheet.set_column(4, 4, 38)

    format_title = workbook.add_format()
    format_title.set_font_size(16)
    worksheet.write('A1', 'Report Statement ' + influencer.capitalize(), format_title)
    date_format = workbook.add_format()
    date_format.set_font_size(12)
    worksheet.write('A2', date_title, date_format)

    header = [{'header': 'Date'}, {'header': 'Person'}, {'header': 'Statement'}, {'header': 'News Title'},
              {'header': 'Source Media'}]
    worksheet.add_table('A5:E' + str(num+5), {'data': data_list, 'columns': header})

    workbook.close()
    return FileResponse(file_location + file_name, media_type='application/octet-stream', filename=file_name)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
