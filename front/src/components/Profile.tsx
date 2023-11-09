import randomColor from "randomcolor";
import { RxAvatar } from "react-icons/rx";

export function Avatar48({ id }: { id: number }) {
  return (
    <RxAvatar
      size={48}
      aria-label={`User ${id}`}
      style={{
        color: randomColor({
          seed: id,
          luminosity: "light",
        }),
      }}
    />
  );
}
