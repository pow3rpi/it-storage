import $ from 'jquery';

import { Config } from '../../config';

export default function normalizeFormFields(...ids) {
  ids.forEach((id) => {
    $('#' + id).val(
      $('#' + id)
        .val()
        .trim()
    );
  });
};

export function normalizeTag(tag) {
  const regExp = new RegExp(`[^a-zA-Z0-9${Config.TAG_ALLOWED_CHARS}]`);
  tag = tag.replace(regExp, '').toLowerCase();

  return tag
}
