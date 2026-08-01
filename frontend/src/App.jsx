import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Leads from './pages/Leads.jsx'
import Profile from './pages/Profile.jsx'
import Team from './pages/Team.jsx'
import './App.css'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Leads />} />
        <Route path="/team" element={<Team />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Layout>
  )
}

export default App
