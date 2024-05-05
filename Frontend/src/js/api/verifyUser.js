import { API_URL } from '../../config';

export default async function verifyUserRequest() {
  const options = {
    method: 'POST',
    credentials: 'include',
  };
  return await fetch(`${API_URL}/verify_user`, options);
};