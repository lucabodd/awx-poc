

def print_head():
    print("""<!DOCTYPE html>
    <html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
       <head>
          <title></title>
          <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
          <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
          <style>
             * {
             box-sizing: border-box;
             }
             body {
             margin: 0;
             padding: 0;
             }
             a[x-apple-data-detectors] {
             color: inherit !important;
             text-decoration: inherit !important;
             }
             #MessageViewBody a {
             color: inherit;
             text-decoration: none;
             }
             p {
             line-height: inherit
             }
             .desktop_hide,
             .desktop_hide table {
             mso-hide: all;
             display: none;
             max-height: 0px;
             overflow: hidden;
             }
             .menu_block.desktop_hide .menu-links span {
             mso-hide: all;
             }
             @media (max-width:920px) {
             .desktop_hide table.icons-inner {
             display: inline-block !important;
             }
             .icons-inner {
             text-align: center;
             }
             .icons-inner td {
             margin: 0 auto;
             }
             .row-content {
             width: 100% !important;
             }
             .mobile_hide {
             display: none;
             }
             .stack .column {
             width: 100%;
             display: block;
             }
             .mobile_hide {
             min-height: 0;
             max-height: 0;
             max-width: 0;
             overflow: hidden;
             font-size: 0px;
             }
             .desktop_hide,
             .desktop_hide table {
             display: table !important;
             max-height: none !important;
             }
             }
          </style>
       </head>""")

def print_header(awx_task_id="https://awx.hqit.kaleyra.com/#/jobs/playbook/{{tower_job_id}}"):
    print("""<body style="background-color: #f6f6f6; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">

          <table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f6f6;" width="100%">
    <tbody>
       <tr>
          <td>
             <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;" width="100%">
                <tbody>
                   <tr>
                      <td>
                         <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
                            <tbody>
                               <tr>
                                  <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                     <table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                        <tr>
                                           <td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:25px;">
                                              <div align="center" class="alignment" style="line-height:10px"><img alt="Alternate text" src="https://www.kaleyra.com/wp-content/uploads/2020/06/Kaleyra-Logo.png" style="display: block; height: auto; border: 0; width: 165px; max-width: 100%;" title="Alternate text" width="165"/></div>
                                           </td>
                                        </tr>
                                     </table>
                                  </td>
                                  <td class="column column-2" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                     <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                        <tr>
                                           <td class="pad" style="padding-bottom:30px;padding-left:10px;padding-right:10px;padding-top:30px;">
                                              <div style="font-family: undefined">
                                                 <div style="font-size:12px; line-height:120%"> </div>
                                              </div>
                                           </td>
                                        </tr>
                                     </table>
                                  </td>
                                  <td class="column column-3" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                     <table border="0" cellpadding="0" cellspacing="0" class="menu_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                        <tr>
                                           <td class="pad" style="color:#e31d37;font-family:inherit;font-size:14px;text-align:center;padding-top:20px;padding-bottom:20px;">
                                              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                                 <tr>
                                                    <td class="alignment" style="text-align:center;font-size:0px;">
                                                                                                               <!-- AWX Job output -->
                                                                                                               <div class="menu-links">
                                                          <!--[if mso]>
                                                          <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="center" style="">
                                                             <tr>
                                                                <td style="padding-top:20px;padding-right:15px;padding-bottom:5px;padding-left:15px">
                                                                   <![endif]--><a href="{}" style="padding-top:20px;padding-bottom:5px;padding-left:15px;padding-right:15px;display:inline-block;color:#e31d37;font-family:Helvetica Neue, Helvetica, Arial, sans-serif;font-size:14px;text-decoration:none;letter-spacing:normal;">AWX Job Output</a>
                                                                   <!--[if mso]>
                                                                </td>
                                                             </tr>
                                                          </table>
                                                          <![endif]-->
                                                       </div>
                                                    </td>
                                                 </tr>
                                              </table>
                                           </td>
                                        </tr>
                                     </table>
                                  </td>
                               </tr>
                            </tbody>
                         </table>
                      </td>
                   </tr>
                </tbody>
             </table>""".format(awx_task_id))

def print_title(title):
    print("""<!-- print title -->
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e31d37;" width="100%">
<tbody>
<tr>
<td>
 <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
    <tbody>
       <tr>
          <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 20px; padding-bottom: 25px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
             <table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                <tr>
                   <td class="pad">
                      <div style="font-family: Arial, sans-serif">
                         <div class="" style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                            <p style="margin: 0; text-align: center; mso-line-height-alt: 14.399999999999999px;"><span style="font-size:34px;"><strong><span style="">{}<br/></span></strong></span></p>
                         </div>
                      </div>
                   </td>
                </tr>
             </table>
          </td>
       </tr>
    </tbody>
 </table>
</td>
</tr>
</tbody>
</table>""".format(title))

def print_subtitle(subtitle):
    print("""
    <!--print subtitle -->
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
 <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
    <tbody>
       <tr>
          <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
             <table border="0" cellpadding="10" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                <tr>
                   <td class="pad">
                      <div style="font-family: Arial, sans-serif">
                         <div class="" style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #e31d37; line-height: 1.2; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                            <p style="margin: 0; text-align: center; mso-line-height-alt: 14.399999999999999px;"><span style="font-size:34px;"><strong><span style="">{}</span></strong></span></p>
                         </div>
                      </div>
                   </td>
                </tr>
             </table>
          </td>
       </tr>
    </tbody>
 </table>
</td>
</tr>
</tbody>
</table>""".format(subtitle))

def print_item_section(section_title):
    print("""
        							 <!-- section -->
                       <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                          <tbody>
                             <tr>
                                <td>
                                   <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; border-bottom: 10px solid transparent; border-left: 10px solid transparent; border-radius: 20px; border-right: 10px solid transparent; border-top: 10px solid transparent; color: #000000; width: 900px;" width="900">
                                      <tbody>
                                         <tr>
                                            <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 40px; padding-bottom: 15px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
                                               <table border="0" cellpadding="5" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                                  <tr>
                                                     <td class="pad">
                                                        <div style="font-family: Arial, sans-serif">
                                                           <div class="" style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #e31d37; line-height: 1.2; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                                                              <p style="margin: 0; text-align: left; mso-line-height-alt: 14.399999999999999px;"><span style="font-size:18px;"><strong>{}</strong></span></p>
                                                           </div>
                                                        </div>
                                                     </td>
                                                  </tr>
                                               </table>
                                               """.format(section_title))

def print_item_description(item_title):
    print("""
<!-- items title -->
<table border="0" cellpadding="5" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: Arial, sans-serif">
<div class="" style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #e31d37; line-height: 1.2; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
<p style="margin: 0; text-align: left; font-size: 10px; mso-line-height-alt: 12px;"><span style="font-size:14px;"><strong>{}</strong></span></p>
</div>
</div>
</td>
</tr>
</table>
<!-- items -->
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; mso-line-height-alt: 18px; color: #000000; line-height: 1.5; font-family: Helvetica Neue, Helvetica, Arial, sans-serif;">
<ul style="list-style-type: circle; line-height: 1.5; mso-line-height-alt: 18px;">    """.format(item_title))

def print_item(item):
    print("""<li style="text-align:left;">{}</li>""".format(item))

def print_item_list_end():
    print("""
        </ul>
     </div>
  </div>
</td>
</tr>
</table>
    """)

def print_item_footer():
    print("""<table border="0" cellpadding="10" cellspacing="0" class="text_block block-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                                  <tr>
                                                     <td class="pad">
                                                        <div style="font-family: undefined">
                                                           <div style="font-size:12px; line-height:120%"> </div>
                                                        </div>
                                                     </td>
                                                  </tr>
                                               </table>
                                            </td>
                                         </tr>
                                      </tbody>
                                   </table>
                                </td>
                             </tr>
                          </tbody>
                       </table>
    """)

def print_spacer():
    print("""
        							 <!-- spacer -->
                       <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                          <tbody>
                             <tr>
                                <td>
                                   <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; border-radius: 0; width: 900px;" width="900">
                                      <tbody>
                                         <tr>
                                            <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
                                               <div class="spacer_block" style="height:60px;line-height:60px;font-size:1px;"> </div>
                                            </td>
                                         </tr>
                                      </tbody>
                                   </table>
                                </td>
                             </tr>
                          </tbody>
                       </table>
    """)

def print_counter_four(one_value, one_title, two_value, two_title, three_value, three_title, four_value, four_title):
    print("""
        <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e31d37;" width="100%">
<tbody>
<tr>
  <td>
     <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
        <tbody>
           <tr>
              <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="25%">
                 <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                    <tr>
                       <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                          <div style="font-family: Arial, sans-serif">
                             <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                             </div>
                          </div>
                       </td>
                    </tr>
                 </table>
              </td>
              <td class="column column-2" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="25%">
                 <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                    <tr>
                       <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                          <div style="font-family: Arial, sans-serif">
                             <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                             </div>
                          </div>
                       </td>
                    </tr>
                 </table>
              </td>
              <td class="column column-3" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="25%">
                 <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                    <tr>
                       <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                          <div style="font-family: Arial, sans-serif">
                             <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                             </div>
                          </div>
                       </td>
                    </tr>
                 </table>
              </td>
              <td class="column column-4" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="25%">
                 <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                    <tr>
                       <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                          <div style="font-family: Arial, sans-serif">
                             <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                             </div>
                          </div>
                       </td>
                    </tr>
                 </table>
              </td>
           </tr>
        </tbody>
     </table>
  </td>
</tr>
</tbody>
</table>
    """.format(one_value, one_title, two_value, two_title, three_value, three_title, four_value, four_title))

def print_counter_three(one_value, one_title, two_value, two_title, three_value, three_title):
    print("""
    							 <!-- counter three -->
                   <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e31d37;" width="100%">
                      <tbody>
                         <tr>
                            <td>
                               <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
                                  <tbody>
                                     <tr>
                                        <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                           <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                              <tr>
                                                 <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                                                    <div style="font-family: Arial, sans-serif">
                                                       <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                                                       </div>
                                                    </div>
                                                 </td>
                                              </tr>
                                           </table>
                                        </td>
                                        <td class="column column-2" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                           <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                              <tr>
                                                 <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                                                    <div style="font-family: Arial, sans-serif">
                                                       <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                                                       </div>
                                                    </div>
                                                 </td>
                                              </tr>
                                           </table>
                                        </td>
                                        <td class="column column-3" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
                                           <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                              <tr>
                                                 <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                                                    <div style="font-family: Arial, sans-serif">
                                                       <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                                          <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                                                       </div>
                                                    </div>
                                                 </td>
                                              </tr>
                                           </table>
                                        </td>
                                     </tr>
                                  </tbody>
                               </table>
                            </td>
                         </tr>
                      </tbody>
                   </table>
    """).format(one_value, one_title, two_value, two_title, three_value, three_title)

def print_counter_two(one_value, one_title, two_value, two_title):
    print("""<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e31d37;" width="100%">
                          <tbody>
                             <tr>
                                <td>
                                   <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
                                      <tbody>
                                         <tr>
                                            <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="50%">
                                               <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                                  <tr>
                                                     <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                                                        <div style="font-family: Arial, sans-serif">
                                                           <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                                              <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                                              <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                                                           </div>
                                                        </div>
                                                     </td>
                                                  </tr>
                                               </table>
                                            </td>
                                            <td class="column column-2" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="50%">
                                               <table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                                                  <tr>
                                                     <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:15px;">
                                                        <div style="font-family: Arial, sans-serif">
                                                           <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                                              <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                                              <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                                                           </div>
                                                        </div>
                                                     </td>
                                                  </tr>
                                               </table>
                                            </td>
                                         </tr>
                                      </tbody>
                                   </table>
                                </td>
                             </tr>
                          </tbody>
                       </table>
    """.format(one_value, one_title, two_value, two_title))

def print_counter_mono(one_value, one_title):
    print("""
        <!-- col mono -->
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #e31d37;" width="100%">
<tbody>
<tr>
  <td>
     <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 900px;" width="900">
        <tbody>
           <tr>
              <td class="column column-1" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
                 <table border="0" cellpadding="10" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                    <tr>
                       <td class="pad">
                          <div style="font-family: Arial, sans-serif">
                             <div class="" style="font-size: 12px; font-family: 'Oswald', Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:96px;">{}</span></p>
                                <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 16.8px;"><span style="font-size:16px;">{}<br/></span></p>
                             </div>
                          </div>
                       </td>
                    </tr>
                 </table>
              </td>
           </tr>
        </tbody>
     </table>
  </td>
</tr>
</tbody>
</table>
    """.format(one_value, one_title))

def print_footer():
    print("""
           </body>
        </html>
    """)
