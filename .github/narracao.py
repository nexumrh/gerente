# Gera a narração (voz feminina pt-BR) e monta o vídeo da instalação por USB.
import asyncio, json, subprocess, os, sys
VIDEO='nexumcell-instalacao-usb-completo.mp4'
CORTES=[0,4.5,9,14,20,25.5,31,36.5,43.5,50,55,60.5,67,71.5]
FALAS=[
 "Olá! Neste vídeo você vai aprender a instalar a trava NexumCell pelo cabo USB, passo a passo.",
 "Antes de começar, separe o computador com o instalador aberto, o cabo USB e o celular novo da venda.",
 "O aparelho precisa estar com Android 8 ou mais novo, zerado de fábrica, sem conta Google e sem outro aplicativo administrador.",
 "Passo um: ative o modo desenvolvedor. No celular, abra Ajustes, depois Sobre o telefone, e toque sete vezes em Número da versão, até aparecer a mensagem: você agora é um desenvolvedor.",
 "Passo dois: ligue a depuração USB. Em Ajustes, abra Opções do desenvolvedor e ligue a chave Depuração USB.",
 "Passo três: conecte o cabo. Ligue o celular no computador e, na tela do celular, toque em Permitir, para autorizar este computador.",
 "Passo quatro: baixe o instalador. No sistema, abra a venda no passo oito, escolha Pelo cabo USB, baixe o arquivo e abra no computador.",
 "Passo cinco: o instalador faz tudo sozinho. Ele confere o Android, a conta e o IMEI do contrato, instala o aplicativo e ativa a proteção. Se ele pedir, confirme o IMEI.",
 "Importante: quando o instalador mostrar aguardando sinal do aparelho, conecte o celular no Wi-Fi ou coloque o chip. Sem internet, ele não dá sinal e a venda não fica verde.",
 "Pronto! Agora é só esperar ficar verde. O sistema recebe o sinal do aparelho, a depuração USB desliga sozinha e você já pode tirar o cabo.",
 "Depois, finalize com o cliente: configure o Wi-Fi e a conta Google dele, confira se a venda está verde no sistema e só então entregue o aparelho.",
 "Se algo der errado e não ficar verde, toque em Refazer instalação. Se continuar, chame o suporte pelo sistema. Atenção: Xiaomi, Redmi e Poco não aceitam o cabo, use o QR Code. E o iPhone tem um processo separado.",
 "Trava NexumCell. Aparelho protegido: pagou, libera. Quitou, solta.",
]
VOZ=os.environ.get('VOZ','pt-BR-FranciscaNeural')
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode().strip())
async def tts(i,t):
    import edge_tts
    await edge_tts.Communicate(t,VOZ,rate='+4%').save(f'f{i}.mp3')
async def main():
    for i,t in enumerate(FALAS): await tts(i,t)
asyncio.run(main())
partes=[]
for i,t in enumerate(FALAS):
    a,b=CORTES[i],CORTES[i+1]; d0=b-a; da=dur(f'f{i}.mp3'); D=max(d0,da+0.9)
    out=f's{i}.mp4'
    subprocess.check_call(['ffmpeg','-v','error','-y','-ss',str(a),'-t',str(d0),'-i',VIDEO,'-i',f'f{i}.mp3',
      '-filter_complex',f'[0:v]tpad=stop_mode=clone:stop_duration={D-d0+0.05},trim=duration={D},setpts=PTS-STARTPTS,fps=30[v];[1:a]adelay=350|350,apad,atrim=duration={D},aresample=44100,aformat=channel_layouts=mono[a]',
      '-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','26','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k',out])
    partes.append(out); print(i,round(d0,1),'->',round(D,1),flush=True)
open('lista.txt','w').write(''.join(f"file '{p}'\n" for p in partes))
subprocess.check_call(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','lista.txt','-c','copy','-movflags','+faststart','saida.mp4'])
print('ok',dur('saida.mp4'))
