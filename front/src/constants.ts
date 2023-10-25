export const URL_BASE = "http://127.0.0.1:8000/";

export class URLS {
  static new_user = `${URL_BASE}auth/user/new/`;
  static get_token = `${URL_BASE}auth/get-token/`;
  static get_events = `${URL_BASE}core/events/all/`;
  static create_event = `${URL_BASE}core/events/new/`;
  static join_event = (event_id: string | number) => `${URL_BASE}core/events/${event_id}/join/`;
  static get_event = (event_id: string | number) => `${URL_BASE}core/events/${event_id}/`;
  static get_full_event = (event_id: string | number) => `${URL_BASE}core/full-events/${event_id}/`;


}