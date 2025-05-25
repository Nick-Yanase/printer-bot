import Image from "next/image";

export interface blurPinkProps {
  className: string
  width: number
  height: number
}
export default function BlurPink(props: blurPinkProps) {
  return (
    <Image
      src={"/blur-pink.svg"}
      alt="blur-purple"
      width={props.width}
      height={props.height}
      className={props.className}
    />
  );
}