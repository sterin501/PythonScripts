//package oracleDBConnection;
import java.sql.*;

 
public class DBConnection {
 
  

 private static final String QUERY1 =  "SELECT * from Config";



public static void main(String[] args) {
                 
             
                       try  {

                              
                             String[] argss=  args[0].split("\\,+");
                             String URL = "jdbc:oracle:thin:@"+argss[0];
                             String SchemaName =     argss[1];
                             String SchemaPass =     argss[2];     

   //System.out.println (  URL + "  " + SchemaName  + "  " + SchemaPass + "...." + args[0]);        

                             Connection con = getConnection(URL,SchemaName,SchemaPass);
                             Statement stmt = con.createStatement();

                          

                //         ResultSet rs = stmt.executeQuery(QUERY1) ;
                         System.out.println("0");
                
        } catch (Exception e) {
            e.printStackTrace();
               System.out.println ( "Error "+e);
        }  



           }

    public static Connection getConnection(String URL,String username,String password) {

        Connection con = null;
                try {
            // load the Driver Class
            Class.forName(("oracle.jdbc.driver.OracleDriver"));
 


            con = DriverManager.getConnection( (URL),
                                               (username),
                                               (password));


        }
         catch (ClassNotFoundException  e) {
            // TODO Auto-generated catch block
            //e.printStackTrace();
        }

        catch (SQLException  e) {
            // TODO Auto-generated catch block
            //e.printStackTrace();
              System.out.println ( "SQLError "+e);  
        }
        return con;
    }
}



