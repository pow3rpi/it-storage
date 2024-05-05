import '../css/preloader.css';

export default function Preloader() {
  return (
    <div className='d-flex justify-content-center'>
      <div className='spinner-border text-primary loading-page' role='status'>
        <span className='visually-hidden'>Loading...</span>
      </div>
    </div>
  );
}

function PreloaderSearch() {
  return (
    <div className='d-flex justify-content-center'>
      <div className='spinner-border text-primary loading-search' role='status'>
        <span className='visually-hidden'>Loading...</span>
      </div>
    </div>
  );
}

function PreloaderNextPage() {
  return (
    <div className='d-flex justify-content-center pb-5'>
      <div className='spinner-border text-primary' role='status'>
        <span className='visually-hidden'>Loading...</span>
      </div>
    </div>
  );
}

export { PreloaderSearch, PreloaderNextPage };
