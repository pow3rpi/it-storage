import picture from '../img/404.jpg';

export default function NotFound() {
  return (
    <div className='d-flex flex-column'>
      <img className='d-block not-found-img' src={picture} alt='Not Found' />
      <h3 className='d-block text-center'>Oops... Page Not Found</h3>
    </div>
  );
}
