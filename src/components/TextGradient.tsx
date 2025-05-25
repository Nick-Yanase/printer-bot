export interface TextGradientProps {
  children: React.ReactNode;
  className?: string;
}

export default function TextGradient(props: TextGradientProps) {
  return (
    <div
      className={`bg-[length:100%_100%]
       bg-clip-text text-transparent w-fit bg-gradient-to-r from-[#6D34FF] to-[#E60076] 
      
        `}
    >
      <p className={props.className}>
        {props.children}
      </p>
    </div>
  );
}