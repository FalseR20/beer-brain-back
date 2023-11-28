import randomColor from "randomcolor";
import { RxAvatar } from "react-icons/rx";
import { Link } from "react-router-dom";

export function Avatar48({ id }: { id: number }) {
  return (<RxAvatar
    size={48}
    aria-label={`User ${id}`}
    style={{
      color: randomColor({
        seed: id, luminosity: "light",
      }),
    }}
  />);
}


export function Avatar({ member }: { member: { id: number } }) {
  return <div
    className={"m-2"} //  border-bottom border-light rounded-2
  >
    <Link to={`/user/${member.id}`}>
      <Avatar48 id={member.id} />
    </Link>
  </div>;
}
