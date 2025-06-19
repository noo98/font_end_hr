function printTable() {
    const table = document.querySelector(".table").outerHTML;
    const newWindow = window.open("", "_blank");
    newWindow.document.write(`
        <html>
        <head>
            <title>Print Table</title>
            <style>
                body { font-family: "Phetsarath OT", sans-serif; padding: 20px; font-size: 12px; }
                table { width: 100%; border-collapse: collapse; font-size: 10px;}
                th, td { border: 1px solid #000; padding: 8px; text-align: center; font-size: 10px;}
                h2 { text-align: center; }
                .header { text-align: center;}
                .footer { display: flex; grid-template-columns: repeat(4, 1fr); justify-content: space-between; margin-top: 15px; }
                .header_title {display: flex; justify-content: space-between;  }
            </style>
        </head>
        <body>
            <div class="header">
                <img src="/static/images/Lao National.png" alt="logo" width="80" height="80">
                <h3>ສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ <br>
                ສັນຕິພາບ ເອກະລາດ ປະຊາທິປະໄຕ ເອກະພາບ ວັດທະນະຖາວອນ</h3>
            </div>
            <div class="header_title">
                <p>ບໍລິສັດ ຂໍ້ມູນຂ່າວສານສິນເຊື່ອແຫ່ງ ສປປ ລາວ</p>
                <p>ນະຄອນຫຼວງວຽງຈັນ, ວັນທີ ${new Date().toLocaleDateString('en-GB', {year: 'numeric',month: '2-digit',day: '2-digit'})}</p>     
            </div>
            <div class="header">
                <h3>ລາຍຊື່ເບີກຈ່າຍເງິນນ້ຳມັນໃຫ້ພະນັກງານ ບໍລິສັດ ຂໍ້ມູນຂ່າວສານສິນເຊື່ອແຫ່ງ ສປປ ລາວ ປະຈຳເດືອນ ${new Date().toLocaleDateString('en-GB',{year: 'numeric',month: '2-digit'})}</h3>
            </div>   
            ${table}
            <div class="footer">
                <div>
                    <h3>ຮອງຜູ້ອຳນວຍການ</h3>
                </div>
                <div>
                    <h3>ຜູ້ກວດກາ</h3>
                </div>
                <div>
                    <h3>ຫົວໜ້າພະແນກ</h3>
                </div>
                <div>
                    <h3>ຜູ້ຄິດໄລ່</h3>
                </div> 
            </div>
        </body>
        </html>
    `);
    newWindow.document.close();
    newWindow.print();
    newWindow.close();
    newWindow.focus();
}

function exportToExcel() {
    const table = document.querySelector(".table");
    const tableHTML = table.outerHTML.replace(/ /g, '%20');
    const filename = 'meal_report.xls';

    const downloadLink = document.createElement("a");
    document.body.appendChild(downloadLink);

    downloadLink.href = 'data:application/vnd.ms-excel,' + tableHTML;
    downloadLink.download = filename;
    downloadLink.click();
    document.body.removeChild(downloadLink);
}