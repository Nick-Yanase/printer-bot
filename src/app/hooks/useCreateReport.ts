import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import { useCallback } from 'react';
import { Impressora } from '../page';

export function usePDFExport() {
  const gerarRelatorioPDF = useCallback((dados: Impressora[]) => {
    const doc = new jsPDF();

    // 🎯 Título
    doc.setFontSize(18);
    doc.text('Relatório de Impressoras', 14, 22);

    // 📅 Data
    const dataAtual = new Date().toLocaleString();
    doc.setFontSize(10);
    doc.text(`Gerado em: ${dataAtual}`, 14, 30);

    // 📄 Cabeçalho da tabela
    const head = [['IP', 'Modelo', 'Número de Série', 'Contador']];

    // 📊 Corpo da tabela (somente impressoras ativas ✅)
    const body = dados
      .filter(({ obs }) => obs === '✅')
      .map(({ ip = '', modelo = '', numero_serie = '', contador = '' }) => [
        ip,
        modelo,
        numero_serie,
        contador,
      ]);

    // 🏗️ Geração da tabela
    autoTable(doc, {
      head,
      body,
      startY: 40,
      styles: {
        fontSize: 10,
        cellPadding: 3,
      },
      headStyles: {
        fillColor: [230, 0, 118], // 🎨 Cor tema
        textColor: [255, 255, 255],
      },
    });

    // 💾 Salvar PDF
    doc.save('relatorio-impressoras.pdf');
  }, []);

  return { gerarRelatorioPDF };
}
