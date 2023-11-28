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
    id: number
    name_letters: string
  };
  datetime: string;
  action: string;
}