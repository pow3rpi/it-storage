import { API_URL } from '../../config';

export default async function logOutRequest() {
  const options = {
    method: 'POST',
    credentials: 'include',
  };
  return await fetch(`${API_URL}/log_out`, options)
    .then((response) => {
      if (response.status === 200) {
        window.location.replace('/');
      }
    });
}