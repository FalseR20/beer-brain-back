const baseUrlEnv = import.meta.env.VITE_DJANGO_URL;

export const URL_BASE =
  typeof baseUrlEnv == "undefined" ? "http://localhost:8000/" : baseUrlEnv;

function url(path: string): string {
  return URL_BASE + path;
}

export class URLS {
  static new_user = url("auth/user/new/");
  static get_token = url("auth/get-token/");
  static get_profile_self = url("profiles/self");
  static get_events = url("core/events/all/");
  static create_event = url("core/events/new/");

  static get_profile = (profile_id: string | number) =>
    url(`profiles/${profile_id}`);

  static join_event = (event_id: string | number) =>
    url(`core/events/${event_id}/join/`);
  static get_event = (event_id: string | number) =>
    url(`core/events/${event_id}/`);
  static get_full_event = (event_id: string | number) =>
    url(`core/full-events/${event_id}/`);
}
