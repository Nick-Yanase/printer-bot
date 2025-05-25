'use client';

import { useState } from 'react';
import TextGradient from '../components/TextGradient';
import Image from 'next/image';
import { IconDownload, IconStackPush } from '@tabler/icons-react';
import { motion, AnimatePresence } from 'framer-motion';
import { BackgroundBeamsWithCollision } from '@/components/ui/background-beams-with-collision';
import Line from '@/components/Line';
import BlurPink from '@/components/BlurPink';

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
  const [progresso, setProgresso] = useState(0);

  async function getAllCounters() {
    setCarregando(true);
    setProgresso(0);
  
    const intervalo = setInterval(() => {
      setProgresso((old) => {
        if (old < 80) {
          return old + 1;
        }
        return old;
      });
    }, 50);
  
    const endpoints = [
      '/api/RICOH-3500',
      '/api/RICOH-3700',
      '/api/RICOH-4500',
      '/api/RICOH-4055',
      '/api/RICOH-MP501',
      '/api/KYOCERA-PRINTER',
      '/api/KYOCERA-M3550'
    ];
  
    const dadosFinais: Impressora[] = [];
  
    try {
      for (const endpoint of endpoints) {
        const res = await fetch(endpoint);
        const data = await res.json();
        dadosFinais.push(...data);
      }
  
      setDados(dadosFinais);
      setProgresso(100);
    } catch (e) {
      console.error('Erro ao buscar dados das impressoras:', e);
      setProgresso(100);
    } finally {
      clearInterval(intervalo);
      setTimeout(() => {
        setCarregando(false);
        setProgresso(0);
      }, 500);
    }
  }
  

  async function getCounter(){
    setCarregando(true);
    setProgresso(0);
    
      const intervalo = setInterval(() => {
        setProgresso((old) => {
          if (old < 80) {
            return old + 1; // Velocidade da barra até 80%
          }
          return old;
        });
      }, 50); // A cada 50ms aumenta 1%
    
      try {
        const res = await fetch('/api/KYOCERA-M3550');
        const dados = await res.json();
    
        setDados(dados);
        setProgresso(100);
      } catch (e) {
        console.error('Erro ao buscar dados das impressoras:', e);
        setProgresso(100);
      } finally {
        clearInterval(intervalo);
        setTimeout(() => {
          setCarregando(false);
          setProgresso(0);
        }, 500);
      }
  }


  const voltar = () => {
    setDados([])
  }
  return (
    
      <main className="h-fit w-full flex flex-col items-center justify-center gap-5 bg-zinc-950 overflow-hidden relative z-10">
        <BlurPink className='absolute -top-[0px] -left-[0px] z-10 pointer-events-none select-none' width={400} height={400}/>
        <AnimatePresence mode="wait">
          <section className={`flex items-center justify-center ${dados.length === 0 ? ' h-screen' : 'my-20 items-start'}`}>
            {carregando ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col items-center justify-center"
              >
                <Image
                  src="/preloader.gif"
                  width={150}
                  height={150}
                  alt="carregando ..."
                  unoptimized
                />
                <div className="w-72 h-2 bg-zinc-800 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-[#E60076]"
                    initial={{ width: 0 }}
                    animate={{ width: `${progresso}%` }}
                    transition={{ ease: 'linear' }}
                  />
                </div>
              </motion.div>
            )
            :
            dados.length === 0 ? (
              // <BackgroundBeamsWithCollision>
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
                  <p className="text-lg">
                    Extraia os contadores e números de série das impressoras!
                  </p>
                  <button
                    onClick={getAllCounters}
                    className="bg-[#E60076] hover:bg-white hover:text-[#E60076] text-lg font-semibold backdrop-blur-2xl flex gap-2 justify-between px-10 py-3 rounded-lg transition-shadow duration-300 ease-linear hover:shadow-[0_0_20px_1px] hover:shadow-[#E60076] cursor-pointer"
                  >
                    <p>Extrair</p>
                    <IconStackPush className="font-semibold" />
                  </button>
                </motion.div>
              // </BackgroundBeamsWithCollision>
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
                      // onClick={buscarDados}
                      className="bg-[#E60076] hover:bg-white hover:text-[#E60076] font-semibold backdrop-blur-2xl flex gap-3 justify-between px-8 py-2 rounded-lg transition-shadow duration-300 ease-linear hover:shadow-[0_0_20px_1px] hover:shadow-[#E60076] cursor-pointer"
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
