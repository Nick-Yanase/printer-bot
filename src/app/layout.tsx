import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"]})


export const metadata: Metadata = {
  title: "Printer bot",
  description: "Bot capta os contadores e numeros de série das impressoras do hospital",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <head>
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon.ico" />
      </head>
      <body
        className={`${inter.className} antialiased bg-zinc-950`}
      >
        {children}
      </body>
    </html>
  );
}
