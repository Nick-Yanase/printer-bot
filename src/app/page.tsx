'use client';

import { useState } from 'react';
import TextGradient from '../components/TextGradient';
import Image from 'next/image';
import {IconCircleCheckFilled, IconDownload, IconLoader, IconStackPush } from '@tabler/icons-react';
import { motion, AnimatePresence } from 'framer-motion';
import Line from '@/components/Line';
import BlurPink from '@/components/BlurPink';
import { usePDFExport } from './hooks/useCreateReport';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export type Impressora = {
  ip: string;
  modelo?: string;
  contador?: string;
  numero_serie?: string;
  obs?: string;
};

export default function Home() {
  const [dados, setDados] = useState<Impressora[]>([]);
  const [carregando, setCarregando] = useState(false);
  const [statusPorImpressora, setStatusPorImpressora] = useState<Record<string, 'loading' | 'ready' | 'error'>>({});
  const impressoras = [
    // { nome: 'RICOH-3500', endpoint: '/api/RICOH-3500' },
    { nome: 'RICOH-3700', endpoint: '/api/RICOH-3700' },
    // { nome: 'RICOH-4500', endpoint: '/api/RICOH-4500' },
    // { nome: 'RICOH-4055', endpoint: '/api/RICOH-4055' },
    // { nome: 'RICOH-MP501', endpoint: '/api/RICOH-MP501' },
    // { nome: 'KYOCERA-PRINTER', endpoint: '/api/KYOCERA-PRINTER' },
    // { nome: 'KYOCERA-M3550', endpoint: '/api/KYOCERA-M3550' },
    // { nome: 'KYOCERA-FS2100', endpoint: '/api/KYOCERA-FS2100' },
    // { nome: 'KYOCERA-M3145', endpoint: '/api/KYOCERA-M3145' },
  ];

  async function getAllCounters() {
    setCarregando(true);
    const dadosFinais: Impressora[] = [];
  
    for (const impressora of impressoras) {
      // Marca como loading
      setStatusPorImpressora(prev => ({
        ...prev,
        [impressora.nome]: 'loading'
      }));
  
      try {
        const res = await fetch(impressora.endpoint);
        const data = await res.json();
  
        dadosFinais.push(...data);
  
        // Marca como ready
        setStatusPorImpressora(prev => ({
          ...prev,
          [impressora.nome]: 'ready'
          
        }));
      } catch (e) {
        console.error(`Erro na ${impressora.nome}:`, e);
        // Marca como erro
        setStatusPorImpressora(prev => ({
          ...prev,
          [impressora.nome]: 'error'
        }));
      }
    }
  
    setDados(dadosFinais);
    setTimeout(()=> {},2000)
    setCarregando(false)
  }
  
  const voltar = () => {
    setDados([])
  }
  const { gerarRelatorioPDF } = usePDFExport()
  return (
      <main className="h-fit w-full flex flex-col items-center justify-center gap-5 bg-zinc-950 overflow-hidden relative z-1">
        <BlurPink className='absolute -top-[0px] -left-[0px] z-10 pointer-events-none select-none' width={400} height={400}/>
        <AnimatePresence mode="wait">
          <section className={`bg-zinc-950 flex items-center justify-center ${dados.length === 0 ? ' h-screen w-full' : 'my-20 items-start'}`}>
            {carregando ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col items-center justify-center"
              >
                <DotLottieReact
                  src="https://lottie.host/ab53042a-8220-4d8e-b5bb-6c201ac188b3/SE71fe9vjA.lottie"
                  loop
                  autoplay
                  className='w-48'
                />

                <div className="w-[700px] flex flex-col gap-2">
                  {impressoras.map((impressora) => (
                    <div key={impressora.nome} className="flex items-center justify-between  border-b border-zinc-800 py-2 text-white w-full">
                      <p className="w-40">{impressora.nome}</p>
                      
                      {statusPorImpressora[impressora.nome] === 'loading' && (
                        <p className="text-zinc-400"><IconLoader className='animate-spin'/></p>
                      )}
                      {statusPorImpressora[impressora.nome] === 'ready' && (
                        <p className="text-green-500"><IconCircleCheckFilled /></p>
                      )}
                      {statusPorImpressora[impressora.nome] === 'error' && (
                        <p className="text-red-500">❌</p>
                      )}
                    </div>
                  ))}
                </div>
        
              </motion.div>
            )
            :
            dados.length === 0 ? (
              <motion.div
                key="home"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col items-center gap-5"
              >
                <div className="flex gap-4 items-center">
                  <Image src={"/printer-bot.svg"} alt="logotipo" width={60} height={60} />
                  <TextGradient className="text-5xl font-semibold">Printer Bot</TextGradient>
                </div>
                <p className="text-lg text-zinc-300">
                  Extraia os contadores e números de série das impressoras!
                </p>
                <button
                  onClick={getAllCounters}
                  className="bg-[#E60076] hover:bg-white text-white hover:text-[#E60076] text-lg font-semibold backdrop-blur-2xl flex gap-2 justify-between px-10 py-3 rounded-lg transition-shadow duration-300 ease-linear hover:shadow-[0_0_20px_1px] hover:shadow-[#E60076] cursor-pointer"
                >
                  <p >Extrair</p>
                  <IconStackPush className="font-semibold" />
                </button>
              </motion.div>
            )
            : 
            (
              <motion.div
                key="dados"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col items-center max-w-[1200px] w-full mt-16 z-30"
              >
                <div className="flex gap-4 items-center cursor-pointer" onClick={voltar}>
                  <Image src={"/printer-bot.svg"} alt="logotipo" width={60} height={60} />
                  <TextGradient className="text-5xl font-semibold">Printer Bot</TextGradient>
                </div>
                <div className='w-full flex justify-end mt-5'>
                  <button
                      onClick={() => {gerarRelatorioPDF(dados)}}
                      className="bg-[#E60076] hover:bg-white text-white hover:text-[#E60076] font-semibold backdrop-blur-2xl flex gap-3 justify-between px-8 py-2 rounded-lg transition-shadow duration-300 ease-linear hover:shadow-[0_0_20px_1px] hover:shadow-[#E60076] cursor-pointer"
                    >
                      <p>Baixar relatório</p>
                      <IconDownload />
                    </button>
                </div>
                <div className='flex gap-2 border-b border-zinc-800 pb-2 text-xl text-[#E2117B] font-semibold w-full mt-5'>
                  <div className='w-48'>
                    <p>IPs</p>
                  </div>
                  <div className='w-48'>
                    <p>Modelo</p>
                  </div>
                  <div className='w-48'>
                    <p>Número de série</p>
                  </div>
                  <div className='w-48'>
                    <p>Contador</p>
                  </div>
                  <div className='w-48'>
                    <p>Observação</p>
                  </div>
                </div>
                {dados.map((item, index) => (
                  <Line key={index} item={item} />
                ))}
              </motion.div>
            )}
          </section>
        </AnimatePresence>
      </main>
      
  );
}
