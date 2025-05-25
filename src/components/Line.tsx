import { Impressora } from "@/app/page"

export interface lineProps{
  item: Impressora
}
export default function Line(props: lineProps){
  const {item} = props
  return(
    <div className='flex gap-2 border-b border-zinc-800 py-2 text-white w-full hover:bg-zinc-900 transition-colors'>
      <div className='w-48'>
        <p >{item.ip}</p>
      </div>
      <div className='w-48'>
        <p >{item.modelo}</p>
      </div>
      <div className='w-48'>
        <p >{item.numero_serie}</p>
      </div>
      <div className='w-48'>
        <p >{item.contador}</p>
      </div>
      <div className="w-[400px]">
        <p className='text-sm truncate'>{item.obs}</p>
      </div>
    </div>
  )
}