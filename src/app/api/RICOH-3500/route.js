import { NextResponse } from "next/server";
import { PythonShell } from "python-shell";

export async function GET() {
  return new Promise((resolve) => {
    let pyshell = new PythonShell("src/scripts/RICOH-3500.py");

    let data = "";

    pyshell.on("message", (message) => {
      data += message;
    });

    pyshell.end((err) => {
      if (err) {
        console.error(err);
        resolve(NextResponse.json({ error: "Erro ao executar o script Python." }, { status: 500 }));
      }

      try {
        const parsed = JSON.parse(data);
        resolve(NextResponse.json(parsed));
      } catch (e) {
        console.error("Erro ao parsear JSON:", e);
        resolve(NextResponse.json({ error: "Falha ao converter resposta do Python." }, { status: 500 }));
      }
    });
  });
}
