import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.IOException;

import java.sql.SQLOutput;
import java.util.DoubleSummaryStatistics;

public class WebScrape
{

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        final String searchQuery = "laptop"; // Change this to your desired search query
        final String url = "https://www.amazon.com/s?k=" + searchQuery;
        try
        {
            Document document = Jsoup.connect(url).get();

            Elements productElements = document.select(".s-result-item");

            for (Element productElement : productElements) {
                String title = productElement.select(".a-text-normal").text();
                String price = productElement.select(".a-price .a-offscreen").text();

                System.out.println("Title: " + title);
                System.out.println("Price: " + price);
                System.out.println("---------------");
            }

        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}
