import { useState } from 'react';

import Alert, { DefaultAlert } from '../components/Alert';
import PasswordForm from '../components/forms/Password';
import ProfileTitle from '../layout/ProfileTitle';

export default function Password() {
  const [alert, setAlert] = useState(DefaultAlert);

  return (
    <div className='container'>
      {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
      <ProfileTitle title='Password' />
      <PasswordForm setAlert={setAlert} />
    </div>
  );
}
