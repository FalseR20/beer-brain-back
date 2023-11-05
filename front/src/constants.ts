export const URL_BASE = "http://192.168.100.5:8000/";

function url(path: string): string {
  return URL_BASE + path;
}

export class URLS {
  static new_user = url("auth/user/new/");
  static get_token = url("auth/get-token/");
  static get_events = url("core/events/all/");
  static create_event = url("core/events/new/");
  static join_event = (event_id: string | number) =>
    url(`core/events/${event_id}/join/`);
  static get_event = (event_id: string | number) =>
    url(`core/events/${event_id}/`);
  static get_full_event = (event_id: string | number) =>
    url(`core/full-events/${event_id}/`);
}
