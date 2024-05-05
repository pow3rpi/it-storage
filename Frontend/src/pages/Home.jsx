import AuthForm from '../components/forms/Auth';

export default function Home() {
  return (
    <div className='container mt-5'>
      <div className='row'>
        <div className='col-12'>
          <h2 className='text-center mb-5 mt-lg-5'>Welcome to IT-Storage!</h2>
        </div>
      </div>
      <AuthForm />
    </div>
  );
}
