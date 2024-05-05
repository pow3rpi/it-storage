import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Home from './pages/Home';
import EmailVerification from './pages/EmailVerification';
import Search from './pages/Search';
import ManageContent from './pages/ManageContent';
import Account from './pages/Account';
import Password from './pages/Password';
import PrivacyPolicy from './pages/PrivacyPolicy';
import Terms from './pages/Terms';
import HelpCenter from './pages/HelpCenter';
import LinkMenu from './pages/LinkMenu';
import LinkCreate from './pages/LinkCreate';
import Link from './pages/Link';
import TutorialMenu from './pages/TutorialMenu';
import TutorialCreate from './pages/TutorialCreate';
import Tutorial from './pages/Tutorial';
import NotFound from './pages/NotFound';
import ProtectedPage from './components/ProtectedPage';


function App() {
  return (
    <>
      <Router>
        <main>
          <Routes>
            <Route exact path='/' element={<Home />} />
            <Route path='/search' element={ProtectedPage(<Search />)} />
            <Route path='/manage_content'>
              <Route index={true} element={ProtectedPage(<ManageContent />)} />
              <Route path='links'>
                <Route index={true} element={ProtectedPage(<LinkMenu />)} />
                <Route path='create' element={ProtectedPage(<LinkCreate />)} />
                <Route path=':id' element={ProtectedPage(<Link />)} />
              </Route>
              <Route path='tutorials'>
                <Route index={true} element={ProtectedPage(<TutorialMenu />)} />
                <Route path='create' element={ProtectedPage(<TutorialCreate />)} />
                <Route path=':id' element={ProtectedPage(<Tutorial />)} />
              </Route>
              <Route path='*' element={ProtectedPage(<NotFound />)} />
            </Route>
            <Route path='/profile'>
              <Route index={true} element={<Navigate to='account' />} />
              <Route path='account' element={ProtectedPage(<Account />)} />
              <Route path='password' element={ProtectedPage(<Password />)} />
              <Route path='*' element={ProtectedPage(<NotFound />)} />
            </Route>
            <Route path='/help_center' element={ProtectedPage(<HelpCenter />)} />
            <Route path='/terms' element={ProtectedPage(<Terms />)} />
            <Route path='/privacy_policy' element={ProtectedPage(<PrivacyPolicy />)} />
            <Route path='/email_verification' element={<EmailVerification />} />
            <Route path='*' element={ProtectedPage(<NotFound />)} />
          </Routes>
        </main>
      </Router>
    </>
  );
}

export default App;
