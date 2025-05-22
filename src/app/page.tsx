'use client';

import { useState } from 'react';

type Impressora = {
  ip: string;
  contador?: string;
  numero_serie?: string;
  obs?: string;
};

export default function Home() {
  const [dados, setDados] = useState<Impressora[]>([]);
  const [carregando, setCarregando] = useState(false);

  async function buscarDados() {
    setCarregando(true);
    try {
      const res = await fetch('/api/RICOH-3500');
      const json = await res.json();
      setDados(json);
    } catch (e) {
      console.error('Erro ao buscar dados:', e);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dados das Impressoras RICOH 3500</h1>

      <button
        onClick={buscarDados}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded mb-4"
      >
        Buscar Dados
      </button>

      {carregando ? (
        <p>Carregando...</p>
      ) : dados.length === 0 ? (
        <p>Nenhum dado carregado.</p>
      ) : (
        <div className="space-y-4">
          {dados.map((item, index) => (
            <div key={index} className="border p-4 rounded shadow">
              <p><strong>IP:</strong> {item.ip}</p>
              {item.obs ? (
                <p className="text-red-500"><strong>Erro:</strong> {item.obs}</p>
              ) : (
                <>
                  <p><strong>Contador:</strong> {item.contador}</p>
                  <p><strong>Número de Série:</strong> {item.numero_serie}</p>
                  <p><strong>OBS:</strong> {item.obs}</p>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
