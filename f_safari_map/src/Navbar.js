import './Navbar.css'; 
const Navbar = () => {
    return ( 
        <nav className="navbar">
            <h1>My Blogs</h1>
            <div className="links">
                <a href="/home" >Home</a>
                <a href="/create" style={{
                    color: '#f1356d',
                    backgroundcolor:'black'
                }}>New Blog</a>
            </div>
        </nav>
    );
}
 
export default Navbar;
