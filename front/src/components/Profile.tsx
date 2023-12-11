import randomColor from "randomcolor";
import { RxAvatar } from "react-icons/rx";
import { Link } from "react-router-dom";
import Template from "./Template.tsx";

export interface IProfile {
  id: number;
  firstName: string;
  lastName: string;
}

export default function Profile() {
  const profile: IProfile = {
    id: 1, firstName: "User", lastName: "1",
  };
  return (<Template>
    <h1>{`${profile.firstName} ${profile.lastName}`}</h1>
    <h3>Avatar and linked avatar</h3>
    <div className={"d-flex flex-row gap-2"}>
      <RoundedAvatar profile={profile} sizeMultiplier={0.4} />
      <RoundedAvatar profile={profile} sizeMultiplier={0.5} />
      <RoundedAvatar profile={profile} sizeMultiplier={1} />
      <RoundedAvatarLink profile={profile} sizeMultiplier={0.4} />
      <RoundedAvatarLink profile={profile} sizeMultiplier={0.5} />
    </div>
  </Template>);
}

interface IAvatarProps {
  profile: IProfile;
  sizeMultiplier: number;
  className?: string;
}

export function RoundedAvatarLink(props: IAvatarProps) {
  const letters = (props.profile.firstName.slice(0, 1) + props.profile.lastName.slice(0, 1)).toUpperCase();
  if (props.className == undefined) {
    props.className = "";
  }
  return (<>
    <Link
      to={`/profile/${props.profile.id}`}
      className={`text-decoration-none border rounded-circle border-secondary text-secondary ${props.className}`}
      style={{
        width: `${props.sizeMultiplier * 7}rem`,
        height: `${props.sizeMultiplier * 7}rem`,
        fontSize: `${props.sizeMultiplier * 3}rem`,
        padding: `${props.sizeMultiplier}rem`,
        textAlign: "center",
      }}
    >
      {letters}
    </Link>
  </>);
}

export function RoundedAvatar({ profile, sizeMultiplier }: IAvatarProps) {
  const letters = (profile.firstName.slice(0, 1) + profile.lastName.slice(0, 1)).toUpperCase();
  return (<>
    <div
      className={"border rounded-circle border-secondary text-secondary"}
      style={{
        width: `${sizeMultiplier * 7}rem`,
        height: `${sizeMultiplier * 7}rem`,
        fontSize: `${sizeMultiplier * 3}rem`,
        padding: `${sizeMultiplier}rem`,
        textAlign: "center",
      }}
    >
      {letters}
    </div>
  </>);
}

// To remove
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
