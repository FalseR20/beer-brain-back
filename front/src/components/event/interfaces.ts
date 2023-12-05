import { IProfile } from "../Profile.tsx";

export interface IEvent {
  id: number;
  date: string;
  description: string;
  is_closed: boolean;
  members: IMember[];
}

interface IMember {
  id: number;
  user: number;
  event: number;
  deposits: IDeposit[];
}

interface IDeposit {
  id: number;
  description: string;
  value: number;
  member: number;
}

export interface IChatElement {
  member: {
    profile: IProfile;
  };
  actions: IChatEvent[];
}

export interface IChatEvent {
  name: string;
  datetime: string;
}
