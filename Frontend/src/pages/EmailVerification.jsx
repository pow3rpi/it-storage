import logo from '../img/logo.png';

export default function EmailVerification() {
  return (
    <div className='container'>
      <div className='row text-center mt-5'>
        <h2>
          Thank you for choosing{' '}
          <img
            src={logo}
            style={{ maxWidth: '40px', maxHeight: '40px' }}
            alt='IT-Storage'
          />{' '}
          IT-Storage
        </h2>
        <div style={{ fontSize: '1.3rem' }}>
          We have sent the verification link to your email.
          <br />
          Please go there and activate your profile.
        </div>
      </div>
    </div>
  );
}
