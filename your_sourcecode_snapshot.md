# snapsplit - snapshot

Created: 2026-11-18 15:41:33

Source root: /home/cm/Dokumente/Arbeiten/0000_DEV/Python/Blender_Addons/snapsplit/snapsplit

## Directory tree (excerpt)

```
snapsplit/
├── __init__.py
├── blender_manifest.toml
├── contact_geometry.py
├── LICENCE.txt
├── localization.py
├── ops_align.py
├── ops_connectors.py
├── ops_freehand.py
├── ops_split.py
├── prefs.py
├── profiles.py
├── README.md
├── seam_data.py
├── seam_migration.py
├── ui.py
└── utils.py
```

## Included source files (code-only snapshot)

The following files are included in the snapshot. Each filename is followed by its content.


---

### LICENCE.txt

```txt
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

The GNU General Public License is a free, copyleft license for
software and other kinds of works.

The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.
```

---

### __init__.py

```py
'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''
# __init__.py

bl_info = {
    "name": "SnapSplit  Print-ready segmentation with connectors",
    "author": "Christoph Medicus",
    "email": "dev@betakontext.de",
    "website": "https://dev.betakontext.de",
    "version": (0, 2, 1),
    "blender": (5, 3, 0),
    "location": "View3D > N-Panel > SnapSplit",
    "description": (
        "Split meshes into printable parts and generate fitting connectors for 3D printing."
    ),
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}

import importlib

import bpy

# Import submodules
from . import localization  # translation data (DICTIONARY), no register() of its own
from . import utils
from . import profiles
from . import prefs
from . import ops_split
from . import ops_connectors
from . import ops_align
from . import ops_freehand
from . import ui

# Set to False for release builds to skip the development hot-reload.
DEV_RELOAD = False

_modules = [
    localization,
    utils,
    profiles,
    prefs,
    ops_split,
    ops_connectors,
    ops_align,
    ops_freehand,
    ui,
]

# Modules whose register() completed successfully (in registration order)
_registered = []


# ---------------------------
# Translations
# ---------------------------

def _unregister_translations():
    """Remove the add-on's translation dictionary (safe to call when not registered)."""
    try:
        bpy.app.translations.unregister(__name__)
    except Exception:
        # Not registered (first start) or translation support not built in: ignore
        pass


def _register_translations():
    """Register localization.DICTIONARY with Blender's translation system.

    A failure here must never prevent the add-on from loading; the UI then
    simply stays in English.
    """
    known = set(bpy.app.translations.locales)
    dictionary = {
        locale: entries
        for locale, entries in localization.DICTIONARY.items()
        if locale in known
    }

    skipped = sorted(set(localization.DICTIONARY) - set(dictionary))
    if skipped:
        print(f"SnapSplit: locales unknown to this Blender build were skipped: {skipped}")

    # Hot-reload safety: drop a stale registration before registering again
    _unregister_translations()
    try:
        bpy.app.translations.register(__name__, dictionary)
    except Exception as exc:
        print(f"SnapSplit: translation registration failed, UI stays English: {exc}")


# ---------------------------
# Registration
# ---------------------------

def register():
    """Register translations and all SnapSplit submodules (hot-reload aware)."""
    # Reload modules during development to pick up edits without restarting Blender
    if DEV_RELOAD:
        for m in _modules:
            try:
                importlib.reload(m)
            except Exception:
                # On first load, reload may fail harmlessly
                pass

    # Translations first, so labels are translatable as soon as the classes exist
    _register_translations()

    _registered.clear()
    try:
        for m in _modules:
            if hasattr(m, "register"):
                m.register()
                _registered.append(m)
    except Exception:
        # Roll back everything that was registered so far, then re-raise
        unregister()
        raise


def unregister():
    """Unregister all submodules in reverse order, then the translations."""
    while _registered:
        m = _registered.pop()
        try:
            m.unregister()
        except Exception as exc:
            # Keep going: one failing module must not block the others
            print(f"SnapSplit: unregister failed in {m.__name__}: {exc}")

    _unregister_translations()


```

---

### contact_geometry.py

```py
"""Resolve current planar mesh contacts independently of seam metadata."""

from mathutils import Vector
import bpy


def _area2(polygon):
    """Return signed twice-area using a translated coordinate frame."""
    if len(polygon) < 3:
        return 0.0

    origin = polygon[0]
    return sum(
        (a - origin).cross(b - origin)
        for a, b in zip(polygon, polygon[1:] + polygon[:1])
    )


def _clip_triangle(subject, triangle):
    """Intersect a convex polygon with a CCW triangle."""
    polygon = list(subject)

    for a, b in zip(triangle, triangle[1:] + triangle[:1]):
        if not polygon:
            break

        edge = b - a
        output = []

        for first, second in zip(
            polygon, polygon[1:] + polygon[:1]
        ):
            distance_first = edge.cross(first - a)
            distance_second = edge.cross(second - a)

            first_inside = distance_first >= 0.0
            second_inside = distance_second >= 0.0

            if first_inside:
                output.append(first)

            if first_inside != second_inside:
                denominator = distance_first - distance_second
                if denominator != 0.0:
                    parameter = distance_first / denominator
                    output.append(
                        first + (second - first) * parameter
                    )

        polygon = output

    return polygon


def _bounds(points):
    """Return a world-space axis-aligned bounding box."""
    return (
        tuple(min(point[i] for point in points) for i in range(3)),
        tuple(max(point[i] for point in points) for i in range(3)),
    )


def _boxes_overlap(first, second, tolerance):
    """Reject triangle pairs whose expanded boxes cannot touch."""
    return all(
        first[0][i] <= second[1][i] + tolerance
        and second[0][i] <= first[1][i] + tolerance
        for i in range(3)
    )


def _world_triangles(obj, depsgraph):
    """Copy evaluated triangles and release Blender's temporary mesh."""
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()

    try:
        if mesh is None:
            return []

        mesh.calc_loop_triangles()
        matrix = evaluated.matrix_world.copy()
        coordinates = [
            matrix @ vertex.co
            for vertex in mesh.vertices
        ]
        triangles = []

        for loop_triangle in mesh.loop_triangles:
            points = [
                coordinates[index].copy()
                for index in loop_triangle.vertices
            ]

            # Geometric world normals include reflections and scaling.
            normal = (points[1] - points[0]).cross(
                points[2] - points[0]
            )
            if normal.length_squared == 0.0:
                continue

            normal.normalize()
            triangles.append((points, normal, _bounds(points)))

        return triangles

    finally:
        evaluated.to_mesh_clear()


def _project_triangle(points, origin, tangent, bitangent):
    """Project a world triangle and normalize its winding."""
    polygon = [
        Vector((
            (point - origin).dot(tangent),
            (point - origin).dot(bitangent),
        ))
        for point in points
    ]

    if _area2(polygon) < 0.0:
        polygon.reverse()

    return polygon


def resolve_current_contact(obj_p, obj_q, tolerance):
    """Return a connector pair tuple for one dominant planar contact.

    Return None when no positive-area planar contact can be established.
    Do not infer contact from object names, history, or bounding boxes alone.
    """
    if (
        obj_p is None
        or obj_q is None
        or obj_p == obj_q
        or obj_p.type != 'MESH'
        or obj_q.type != 'MESH'
    ):
        return None

    tolerance = float(tolerance)
    if tolerance <= 0.0:
        raise ValueError("Contact tolerance must be positive.")

    depsgraph = bpy.context.evaluated_depsgraph_get()
    first_triangles = _world_triangles(obj_p, depsgraph)
    second_triangles = _world_triangles(obj_q, depsgraph)

    if not first_triangles or not second_triangles:
        return None

    groups = []
    angular_tolerance = 1e-6
    minimum_area = tolerance * tolerance

    for first, first_normal, first_box in first_triangles:
        origin = first[0]

        # Choose the longest edge for a stable projection frame.
        tangent = max(
            (
                first[1] - first[0],
                first[2] - first[1],
                first[0] - first[2],
            ),
            key=lambda edge: edge.length_squared,
        ).normalized()
        bitangent = first_normal.cross(tangent).normalized()

        first_2d = _project_triangle(
            first, origin, tangent, bitangent
        )

        for second, second_normal, second_box in second_triangles:
            if first_normal.dot(second_normal) > (
                -1.0 + angular_tolerance
            ):
                continue

            if not _boxes_overlap(
                first_box, second_box, tolerance
            ):
                continue

            # Check both planes to avoid accepting tilted near-intersections.
            if any(
                abs((point - origin).dot(first_normal)) > tolerance
                for point in second
            ):
                continue

            if any(
                abs((point - second[0]).dot(second_normal)) > tolerance
                for point in first
            ):
                continue

            second_2d = _project_triangle(
                second, origin, tangent, bitangent
            )
            intersection = _clip_triangle(first_2d, second_2d)
            area = abs(_area2(intersection)) * 0.5

            if area <= minimum_area:
                continue

            # A convex intersection's vertex average lies inside it.
            center_2d = sum(intersection, Vector((0.0, 0.0)))
            center_2d /= len(intersection)
            center = (
                origin
                + tangent * center_2d.x
                + bitangent * center_2d.y
            )

            group = next(
                (
                    candidate
                    for candidate in groups
                    if (
                        candidate["normal"].dot(first_normal)
                        >= 1.0 - angular_tolerance
                        and abs(
                            (origin - candidate["origin"]).dot(
                                candidate["normal"]
                            )
                        ) <= tolerance
                    )
                ),
                None,
            )

            if group is None:
                group = {
                    "origin": origin.copy(),
                    "normal": first_normal.copy(),
                    "area": 0.0,
                    "largest_area": 0.0,
                    "center": center.copy(),
                    "tangent": tangent.copy(),
                }
                groups.append(group)

            group["area"] += area

            if area > group["largest_area"]:
                group["largest_area"] = area
                group["center"] = center.copy()
                group["tangent"] = tangent.copy()

    if not groups:
        return None

    group = max(groups, key=lambda candidate: candidate["area"])
    normal = group["normal"].copy()
    tangent = group["tangent"].copy()

    # P's outward normal points from P's material toward Q's material.
    pin = obj_p
    socket = obj_q

    # Keep role assignment stable relative to the dominant world axis.
    dominant_index = max(range(3), key=lambda i: abs(normal[i]))
    if normal[dominant_index] < 0.0:
        normal.negate()
        pin, socket = socket, pin

    tangent -= normal * tangent.dot(normal)
    tangent.normalize()

    center = group["center"]
    axis = ("X", "Y", "Z")[dominant_index]

    return (
        socket,
        pin,
        axis,
        float(center[dominant_index]),
        1,
        (center, normal, tangent),
    )
```

---

### localization.py

```py
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# localizations.py

DICTIONARY = {
    "de_DE": {
        ("*", "Adjust split axis"): "Schnittachse anpassen",
        ("Operator", "Adjust split axis"): "Schnittachse anpassen",
        ("*", "Split axis adjusted."): "Schnittachse angepasst.",
        ("*", "Adjust split axis cancelled."): "Anpassen der Schnittachse abgebrochen.",
        ("*", "Planar Split"): "Planarer Schnitt",
        ("Operator", "Planar Split"): "Planarer Schnitt",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Das Aufteilen in viele Teile kann bei dichten Meshes eine Weile dauern...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Automatisches Verschließen fand keine gültigen Schleifen.",
        ("*", "Auto-capped seams on {n} part(s)."): "Nähte automatisch bei {n} Teil(en) verschlossen.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Weniger Teile erzeugt als erwartet ({have} < {want}).",
        ("*", "{n} parts created."): "{n} Teile erzeugt.",
        ("*", "Cap seams now"): "Nähte jetzt verschließen",
        ("Operator", "Cap seams now"): "Nähte jetzt verschließen",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Zwischen genau zwei Schnittkanten-Schleifen (außen+innen) pro Ebene füllen. Seeds werden bevorzugt.",
        ("*", "Only selected objects"): "Nur ausgewählte Objekte",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = alle Ebenen pro Objekt, 1 = nur größte",
        ("*", "Select only (no fill)"): "Nur auswählen (nicht füllen)",
        ("*", "Require exactly two seed edges"): "Genau zwei Seed-Kanten erforderlich",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Wenn genau zwei Kanten im Edit-Modus ausgewählt sind, nur diese als Seeds verwenden (keine Auto-Erkennung).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Keine Mesh-Objekte zum Verschließen. Teile auswählen oder die Teile-Kollektion verwenden.",
        ("*", "Processing failed on '{name}': {err}"): "Verarbeitung bei '{name}' fehlgeschlagen: {err}",
        ("*", "Could not determine split edge loops to select."): "Konnte die Schnittkanten-Schleifen nicht zur Auswahl bestimmen.",
        ("*", "Could not determine and fill split edge loops."): "Konnte die Schnittkanten-Schleifen nicht bestimmen und füllen.",
        ("*", "Selected split edge loops on {n} object(s)."): "Schnittkanten-Schleifen bei {n} Objekt(en) ausgewählt.",
        ("*", "Capped seams on {n} object(s)."): "Nähte bei {n} Objekt(en) verschlossen.",
        ("*", "Please select a mesh object."): "Bitte ein Mesh-Objekt auswählen.",
        ("*", "Object has unapplied transforms"): "Objekt hat nicht angewendete Transformationen",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Für exakte und vorhersagbare Ergebnisse ggf. 'Alle Transformationen anwenden' (Strg+A).",
        ("*", "Split Offset (mm)"): "Schnitt-Offset (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Versatz der Schnittebene entlang der Schnittachse (positiv in Achsrichtung)",
        ("*", "Split Axis"): "Schnittachse",
        ("*", "Split along X"): "Entlang X schneiden",
        ("*", "Split along Y"): "Entlang Y schneiden",
        ("*", "Split along Z"): "Entlang Z schneiden",
        ("*", "Show split preview"): "Schnittvorschau anzeigen",
        ("*", "Show temporary orange planes at planned cut positions"): "Temporäre orange Ebenen an geplanten Schnittpositionen anzeigen",
        ("*", "Number of Parts"): "Anzahl Teile",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Gewünschte Segmentanzahl (Schnittebenen = Teile - 1)",
        ("*", "Cap seams during split"): "Nähte während des Schnitts verschließen",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Nähte nach dem Schneiden automatisch schließen. Mit Hohlraum/Innenhülle: präzises Füllen äußerer/innerer Schleifen; ohne Hohlraum: einfaches Füllen. Kann die Laufzeit erhöhen.",
        ("*", "Connector Type"): "Verbinder-Typ",
        ("*", "Cylinder Pin"): "Zylinderstift",
        ("*", "Dowel pin + socket"): "Passstift + Buchse",
        ("*", "Rectangular Tenon"): "Rechteck-Zapfen",
        ("*", "Anti-rotation joint"): "Verdrehsicheres Gelenk",
        ("*", "Dovetail"): "Schwalbenschwanz",
        ("*", "Tapered wedge connector"): "Verjüngter Keilverbinder",
        ("*", "Snap Pin"): "Schnappstift",
        ("*", "Connector with snap spheres"): "Verbinder mit Schnappkugeln",
        ("*", "Snap Tenon"): "Schnapp-Zapfen",
        ("*", "Rectangular tenon with snap spheres"): "Rechteck-Zapfen mit Schnappkugeln",
        ("*", "Snap Dovetail"): "Schnapp-Schwalbenschwanz",
        ("*", "Tapered wedge connector with snap spheres"): "Schwalbenschwanz-Verbinder mit Schnappkugeln",
        ("*", "Custom Connector"): "Benutzerdefinierter Verbinder",
        ("*", "Use another mesh object from the scene as connector shape"): "Verwendet ein anderes Mesh-Objekt aus der Szene als Verbinder-Form",
        ("*", "Select connector object"): "Verbinder-Objekt auswählen",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Mesh-Objekt aus dieser Szene, das als Verbinder-Form verwendet wird. Die lokale Z-Achse gilt als Einsteckrichtung; das Objekt wird auf die unten eingestellten Breite/Länge/Tiefe skaliert.",
        ("*", "Custom Width (mm)"): "Breite (mm)",
        ("*", "Target size along the object's local X axis"): "Zielgröße entlang der lokalen X-Achse des Objekts",
        ("*", "Custom Length (mm)"): "Länge (mm)",
        ("*", "Target size along the object's local Y axis"): "Zielgröße entlang der lokalen Y-Achse des Objekts",
        ("*", "Custom Depth (mm)"): "Tiefe (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Zielgröße entlang der lokalen Z-Achse des Objekts (Einstecktiefe)",
        ("*", "Please select a connector object for Custom Connector."): "Bitte ein Verbinder-Objekt für den benutzerdefinierten Verbinder auswählen.",
        ("*", "Selected connector object has no usable mesh data."): "Das ausgewählte Verbinder-Objekt enthält keine verwertbaren Mesh-Daten.",
        ("*", "Base size"): "Basisgröße",
        ("*", "Dovetail Width (mm)"): "Schwalbenschwanz-Breite (mm)",
        ("*", "Dovetail Length (mm)"): "Schwalbenschwanz-Länge (mm)",
        ("*", "Length along seam plane (local v)"): "Länge entlang der Nahtebene (lokal v)",
        ("*", "Dovetail Depth (mm)"): "Schwalbenschwanz-Tiefe (mm)",
        ("*", "Taper (%)"): "Verjüngung (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Prozentualer Anteil, um den die Spitze schmaler als die Basis ist",
        ("*", "Signed Taper (%)"): "Vorzeichenbehaftete Verjüngung (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Vorzeichenbehaftete Verjüngung entlang der Einstecktrichtung. Positiv verbreitert, negativ verschmälert. Bei Wert ungleich 0 überschreibt dies die einfache Verjüngung.",
        ("*", "Span Axis"): "Spannachse",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Auto dehnt entlang der Schwalbenschwanz-Breitenachse und schneidet zu den Außenseiten; X/Y/Z erzwingen einen Überstand entlang dieser Weltachse, sofern sie in der Nahtebene liegt; Keine verwendet die manuell eingestellte Schwalbenschwanz-Länge",
        ("*", "None"): "Keine",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Verwendet die manuell eingestellte Schwalbenschwanz-Länge; Kanten werden nur beschnitten, wenn Harter Seitenschnitt aktiviert ist",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Automatisch entlang der Schwalbenschwanz-Breitenachse dehnen und zu den Außenseiten schneiden",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Überstand entlang der Weltachse X erzwingen, sofern sie in der Nahtebene liegt",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Überstand entlang der Weltachse Y erzwingen, sofern sie in der Nahtebene liegt",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Überstand entlang der Weltachse Z erzwingen, sofern sie in der Nahtebene liegt",
        ("*", "Forces hard-side cut along this axis."): "Erzwingt einen harten Seitenschnitt entlang dieser Achse.",
        ("*", "Hard-side Cut"): "Harter Seitenschnitt",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Bevorzugt einen scharfen Seitenschnitt für Schwalbenschwanz-Buchse/-Nut",
        ("*", "Margin (%)"): "Rand (%)",
        ("*", "Trim percentage at both ends of seam span"): "Beschnitt-Prozentsatz an beiden Enden der Nahtspanne",
        ("*", "Placement"): "Platzierung",
        ("*", "Offset along Width (mm)"): "Versatz entlang Breite (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Versatz innerhalb der Schnittebene entlang der Breiten-Achse (u), um das Schwalbenschwanz-Muster zu verschieben",
        ("*", "Offset along Length (mm)"): "Versatz entlang Länge (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Versatz innerhalb der Schnittebene entlang der Längen-Achse (v), um das Schwalbenschwanz-Muster zu verschieben",
        ("*", "Rotation in plane (deg)"): "Rotation in der Ebene (Grad)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotation innerhalb der Schnittebene zur Ausrichtung des Schwalbenschwanz-Musters",
        ("*", "Span Mode"): "Spannmodus",
        ("*", "How the dovetail spans along the seam"): "Wie der Schwalbenschwanz die Naht überspannt",
        ("*", "Auto"): "Automatisch",
        ("*", "Use full edge-to-edge span of the seam"): "Volle Kante-zu-Kante-Spanne der Naht verwenden",
        ("*", "Fixed"): "Fest",
        ("*", "Use a fixed repeating spacing"): "Einen festen, sich wiederholenden Abstand verwenden",
        ("*", "Centered"): "Zentriert",
        ("*", "Center block(s) with margins"): "Block(s) mit Rändern zentrieren",
        ("*", "Live Preview"): "Live-Vorschau",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Zeigt eine Live-Drahtgitter-Vorschau der Verbinder-Platzierung (Linie/Raster) für die aktuelle Auswahl. Aus Performance-Gründen auf 200 Vorschau-Objekte begrenzt.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Die Live-Vorschau der Verbinder wurde bei 200 Objekten gestoppt; weitere Punkte werden nicht angezeigt.",
        ("*", "Distribution"): "Verteilung",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Verbinder entlang einer Linie oder in einem Raster über die Nahtfläche verteilen",
        ("*", "Line"): "Linie",
        ("*", "Place connectors along a line in the seam face"): "Verbinder entlang einer Linie in der Nahtfläche platzieren",
        ("*", "Grid"): "Raster",
        ("*", "Distribute connectors in a grid over the seam face"): "Verbinder in einem Raster über die Nahtfläche verteilen",
        ("*", "Connectors per Seam"): "Verbinder pro Naht",
        ("*", "Rows (GRID)"): "Zeilen (RASTER)",
        ("*", "Number of rows for grid distribution"): "Anzahl der Zeilen für die Rasterverteilung",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Randabstand entlang der Naht (und senkrecht im RASTER) als Prozent der Teil-Länge (0–40 % empfohlen)",
        ("*", "Spheres per side"): "Kugeln pro Seite",
        ("*", "Number of snap spheres per side/around"): "Anzahl der Schnappkugeln pro Seite/Umfang",
        ("*", "Sphere Diameter (mm)"): "Kugeldurchmesser (mm)",
        ("*", "Diameter of snap spheres"): "Durchmesser der Schnappkugeln",
        ("*", "Protrusion (mm)"): "Überstand (mm)",
        ("*", "How far spheres protrude from side surface"): "Wie weit die Kugeln aus der Seitenfläche hervortreten",
        ("*", "Pin Diameter (mm)"): "Stiftdurchmesser (mm)",
        ("*", "Pin Length (mm)"): "Stiftlänge (mm)",
        ("*", "Segments"): "Segmente",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Zylinderstift-Radialsegmente (optische Glätte)",
        ("*", "Tenon Width (mm)"): "Zapfenbreite (mm)",
        ("*", "Tenon Depth (mm)"): "Zapfentiefe (mm)",
        ("*", "Chamfer (mm)"): "Fase (mm)",
        ("*", "Insert Depth (%)"): "Einstecktiefe (%)",
        ("*", "Percentage of connector length recessed into part A"): "Prozentualer Anteil der Verbinderlänge, der in Teil A versenkt wird",
        ("*", "Material Profiles"): "Material-Profile",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Materialprofil wählen, um Toleranz pro Seite automatisch zu befüllen",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Empfohlene Toleranz pro Seite: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Toleranz pro Fläche (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Überschreibt das Materialprofil (0 = Profilwert verwenden)",
        ("*", "More segmentation settings"): "Weitere Segmentierungs-Einstellungen",
        ("*", "Show advanced segmentation options"): "Erweiterte Segmentierungsoptionen anzeigen",
        ("*", "More connection settings"): "Weitere Verbindungs-Einstellungen",
        ("*", "Show advanced connection/geometry options"): "Erweiterte Verbindungs-/Geometrieoptionen anzeigen",
        ("*", "More tolerance settings"): "Weitere Toleranz-Einstellungen",
        ("*", "Show advanced tolerance options"): "Erweiterte Toleranzoptionen anzeigen",
        ("*", "More alignment settings"): "Weitere Ausrichtungs-Einstellungen",
        ("*", "Show advanced alignment options"): "Erweiterte Ausrichtungsoptionen anzeigen",
        ("*", "Segmentation"): "Segmentierung",
        ("*", "Less..."): "Weniger...",
        ("*", "Adjust"): "Anpassen",
        ("*", "Connections"): "Verbindungen",
        ("*", "Add connectors"): "Verbinder hinzufügen",
        ("Operator", "Add connectors"): "Verbinder hinzufügen",
        ("*", "Place connectors (click)"): "Verbinder platzieren (Klick)",
        ("Operator", "Place connectors (click)"): "Verbinder platzieren (Klick)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Flächen im Objektmodus wählen (A = Ziel, B = beweglich)",
        ("*", "A: none"): "A: keine",
        ("*", "B: none"): "B: keine",
        ("*", "Pick Face A"): "Fläche A wählen",
        ("Operator", "Pick Face A"): "Fläche A wählen",
        ("*", "Pick Face B"): "Fläche B wählen",
        ("Operator", "Pick Face B"): "Fläche B wählen",
        ("*", "Align Faces"): "Flächen ausrichten",
        ("Operator", "Align Faces"): "Flächen ausrichten",
    },
    "fr_FR": {
        ("*", "Adjust split axis"): "Ajuster l'axe de coupe",
        ("Operator", "Adjust split axis"): "Ajuster l'axe de coupe",
        ("*", "Split axis adjusted."): "Axe de coupe ajusté.",
        ("*", "Adjust split axis cancelled."): "Ajustement de l'axe de coupe annulé.",
        ("*", "Planar Split"): "Découpe planaire",
        ("Operator", "Planar Split"): "Découpe planaire",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Découper en de nombreuses pièces peut prendre du temps sur des maillages denses...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Le bouchage automatique n'a trouvé aucune boucle valide.",
        ("*", "Auto-capped seams on {n} part(s)."): "Bouchage automatique des arêtes sur {n} pièce(s).",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Moins de pièces créées que prévu ({have} < {want}).",
        ("*", "{n} parts created."): "{n} pièces créées.",
        ("*", "Cap seams now"): "Boucher les arêtes maintenant",
        ("Operator", "Cap seams now"): "Boucher les arêtes maintenant",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Remplir entre exactement deux boucles d'arêtes de coupe (externe+interne) per plan. Seeds privilégiés.",
        ("*", "Only selected objects"): "Objets sélectionnés uniquement",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = tous les plans per objet, 1 = seulement le plus grand",
        ("*", "Select only (no fill)"): "Sélectionner seulement (sans remplissage)",
        ("*", "Require exactly two seed edges"): "Exiger exactement deux arêtes seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Si exactement deux arêtes sont sélectionnées en mode Édition, les utiliser uniquement comme seeds (pas d'auto-détection).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Aucun objet maillage à boucher. Sélectionnez des pièces découpées ou utilisez la collection des pièces.",
        ("*", "Processing failed on '{name}': {err}"): "Échec du traitement sur « {name} » : {err}",
        ("*", "Could not determine split edge loops to select."): "Impossible de déterminer les boucles d'arêtes de coupe à sélectionner.",
        ("*", "Could not determine and fill split edge loops."): "Impossible de déterminer et de remplir les boucles d'arêtes de coupe.",
        ("*", "Selected split edge loops on {n} object(s)."): "Boucles d'arêtes de coupe sélectionnées sur {n} objet(s).",
        ("*", "Capped seams on {n} object(s)."): "Arêtes bouchées sur {n} objet(s).",
        ("*", "Please select a mesh object."): "Veuillez sélectionner un objet maillage.",
        ("*", "Object has unapplied transforms"): "L'objet a des transformations non appliquées",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Envisagez d'appliquer toutes les transformations (Ctrl+A) pour des résultats précis et prévisibles.",
        ("*", "Split Offset (mm)"): "Décalage de coupe (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Décalage du plan de coupe le long de l'axe (positif dans le sens de l'axe)",
        ("*", "Split Axis"): "Axe de coupe",
        ("*", "Split along X"): "Couper selon X",
        ("*", "Split along Y"): "Couper selon Y",
        ("*", "Split along Z"): "Couper selon Z",
        ("*", "Show split preview"): "Afficher l'aperçu de coupe",
        ("*", "Show temporary orange planes at planned cut positions"): "Afficher des plans orange temporaires aux positions de coupe prévues",
        ("*", "Number of Parts"): "Nombre de pièces",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Nombre de segments souhaités (plans de coupe = pièces - 1)",
        ("*", "Cap seams during split"): "Boucher les arêtes pendant la coupe",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Fermer automatiquement les arêtes après la coupe. Avec cavité/coque interne : remplissage précis des boucles externe/interne ; sans cavité : remplissage simple. Peut augmenter le temps d'exécution.",
        ("*", "Connector Type"): "Type de connecteur",
        ("*", "Cylinder Pin"): "Goujon cylindrique",
        ("*", "Dowel pin + socket"): "Goujon + douille",
        ("*", "Rectangular Tenon"): "Tenon rectangulaire",
        ("*", "Anti-rotation joint"): "Articulation anti-rotation",
        ("*", "Dovetail"): "Queue d'aronde",
        ("*", "Tapered wedge connector"): "Connecteur en coin conique",
        ("*", "Snap Pin"): "Goujon à encliqueter",
        ("*", "Connector with snap spheres"): "Connecteur avec billes d'encliquetage",
        ("*", "Snap Tenon"): "Tenon à encliqueter",
        ("*", "Rectangular tenon with snap spheres"): "Tenon rectangulaire avec billes d'encliquetage",
        ("*", "Snap Dovetail"): "Queue d'aronde à encliquetage",
        ("*", "Tapered wedge connector with snap spheres"): "Connecteur en coin conique avec billes d'encliquetage",
        ("*", "Custom Connector"): "Connecteur personnalisé",
        ("*", "Use another mesh object from the scene as connector shape"): "Utiliser un autre objet maillage de la scène comme forme de connecteur",
        ("*", "Select connector object"): "Sélectionner l'objet connecteur",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Objet maillage de cette scène utilisé comme forme de connecteur. Son axe Z local est traité comme la direction d'insertion ; il sera redimensionné selon les valeurs Largeur/Longueur/Profondeur ci-dessous.",
        ("*", "Custom Width (mm)"): "Largeur personnalisée (mm)",
        ("*", "Target size along the object's local X axis"): "Taille cible le long de l'axe X local de l'objet",
        ("*", "Custom Length (mm)"): "Longueur personnalisée (mm)",
        ("*", "Target size along the object's local Y axis"): "Taille cible le long de l'axe Y local de l'objet",
        ("*", "Custom Depth (mm)"): "Profondeur personnalisée (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Taille cible le long de l'axe Z local de l'objet (profondeur d'insertion)",
        ("*", "Please select a connector object for Custom Connector."): "Veuillez sélectionner un objet connecteur pour le connecteur personnalisé.",
        ("*", "Selected connector object has no usable mesh data."): "L'objet connecteur sélectionné ne contient pas de données de maillage utilisables.",
        ("*", "Base size"): "Taille de base",
        ("*", "Dovetail Width (mm)"): "Largeur de la queue d'aronde (mm)",
        ("*", "Dovetail Length (mm)"): "Longueur de la queue d'aronde (mm)",
        ("*", "Length along seam plane (local v)"): "Longueur le long du plan de la couture (v local)",
        ("*", "Dovetail Depth (mm)"): "Profondeur de la queue d'aronde (mm)",
        ("*", "Taper (%)"): "Conicité (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Pourcentage selon lequel la pointe est plus étroite que la base",
        ("*", "Signed Taper (%)"): "Conicité signée (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Conicité signée le long de l'insertion. Positif élargit, négatif rétrécit. Si différent de zéro, remplace la conicité simple.",
        ("*", "Span Axis"): "Axe d'étendue",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Auto étire le long de l'axe de largeur de la queue d'aronde et coupe jusqu'aux côtés extérieurs ; X/Y/Z forcent un dépassement le long de cet axe monde s'il se trouve dans le plan de la couture ; Aucun utilise la longueur configurée manuellement",
        ("*", "None"): "Aucun",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Utiliser la longueur de queue d'aronde configurée manuellement ; ne couper les bords que si la coupe à bord dur est activée",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Étirer automatiquement le long de l'axe de largeur de la queue d'aronde et couper jusqu'aux côtés extérieurs",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Forcer le dépassement le long de l'axe monde X, s'il se trouve dans le plan de la couture",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Forcer le dépassement le long de l'axe monde Y, s'il se trouve dans le plan de la couture",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Forcer le dépassement le long de l'axe monde Z, s'il se trouve dans le plan de la couture",
        ("*", "Forces hard-side cut along this axis."): "Force une coupe à bord dur le long de cet axe.",
        ("*", "Hard-side Cut"): "Coupe à bord dur",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Préférer une coupe nette des côtés pour l'emboîture/rainure de la queue d'aronde",
        ("*", "Margin (%)"): "Marge (%)",
        ("*", "Trim percentage at both ends of seam span"): "Pourcentage de rognage aux deux extrémités de l'étendue de la couture",
        ("*", "Placement"): "Placement",
        ("*", "Offset along Width (mm)"): "Décalage le long de la largeur (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Décalage dans le plan de coupe le long de l'axe de largeur (u) pour déplacer le motif de la queue d'aronde",
        ("*", "Offset along Length (mm)"): "Décalage le long de la longueur (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Décalage dans le plan de coupe le long de l'axe de longueur (v) pour déplacer le motif de la queue d'aronde",
        ("*", "Rotation in plane (deg)"): "Rotation dans le plan (deg)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotation dans le plan de coupe pour orienter le motif de la queue d'aronde",
        ("*", "Span Mode"): "Mode d'étendue",
        ("*", "How the dovetail spans along the seam"): "Comment la queue d'aronde s'étend le long de la couture",
        ("*", "Auto"): "Auto",
        ("*", "Use full edge-to-edge span of the seam"): "Utiliser l'étendue complète bord à bord de la couture",
        ("*", "Fixed"): "Fixe",
        ("*", "Use a fixed repeating spacing"): "Utiliser un espacement fixe répété",
        ("*", "Centered"): "Centré",
        ("*", "Center block(s) with margins"): "Centrer le(s) bloc(s) avec des marges",
        ("*", "Live Preview"): "Aperçu en direct",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Afficher un aperçu filaire en direct du placement des connecteurs (Ligne/Grille) pour la sélection actuelle. Limité à 200 objets d'aperçu pour des raisons de performance.",
        ("*", "Connector live preview stopped at {cap} objects; remaining points are not shown."): "L'aperçu en direct des connecteurs s'est arrêté à 200 objets ; les points restants ne sont pas affichés.",
        ("*", "Distribution"): "Répartition",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Répartir les connecteurs le long d'une ligne ou en grille sur la surface de la couture",
        ("*", "Line"): "Ligne",
        ("*", "Place connectors along a line in the seam face"): "Placer les connecteurs le long d'une ligne dans la surface de la couture",
        ("*", "Grid"): "Grille",
        ("*", "Distribute connectors in a grid over the seam face"): "Répartir les connecteurs en grille sur la surface de la couture",
        ("*", "Connectors per Seam"): "Connecteurs par couture",
        ("*", "Rows (GRID)"): "Rangées (GRILLE)",
        ("*", "Number of rows for grid distribution"): "Nombre de rangées pour la répartition en grille",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Marge de bord le long de la couture (et perpendiculaire en GRILLE) en pourcentage de la longueur de la pièce (0–40 % recommandé)",
        ("*", "Spheres per side"): "Billes par côté",
        ("*", "Number of snap spheres per side/around"): "Nombre de billes d'encliquetage par côté/pourtour",
        ("*", "Sphere Diameter (mm)"): "Diamètre bille (mm)",
        ("*", "Diameter of snap spheres"): "Diamètre des billes d'encliquetage",
        ("*", "Protrusion (mm)"): "Saillie (mm)",
        ("*", "How far spheres protrude from side surface"): "De combien les billes dépassent de la surface latérale",
        ("*", "Pin Diameter (mm)"): "Diamètre du goujon (mm)",
        ("*", "Pin Length (mm)"): "Longueur du goujon (mm)",
        ("*", "Segments"): "Segments",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segments radiaux du goujon cylindrique (lissage visuel)",
        ("*", "Tenon Width (mm)"): "Largeur du tenon (mm)",
        ("*", "Tenon Depth (mm)"): "Profondeur du tenon (mm)",
        ("*", "Chamfer (mm)"): "Chanfrein (mm)",
        ("*", "Insert Depth (%)"): "Profondeur d'insertion (%)",
        ("*", "Percentage of connector length recessed into part A"): "Pourcentage de la longueur du connecteur encastré dans la pièce A",
        ("*", "Material Profiles"): "Profils de matériau",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Sélectionner un profil matériau pour préremplir la tolérance par côté",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Tolérance recommandée par côté : {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolérance par face (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Passe outre le profil matériau (0 = utiliser la valeur du profil)",
        ("*", "More segmentation settings"): "Plus de réglages de segmentation",
        ("*", "Show advanced segmentation options"): "Afficher les options avancées de segmentation",
        ("*", "More connection settings"): "Plus de réglages de connexion",
        ("*", "Show advanced connection/geometry options"): "Afficher les options avancées de connexion/géométrie",
        ("*", "More tolerance settings"): "Plus de réglages de tolérance",
        ("*", "Show advanced tolerance options"): "Afficher les options avancées de tolérance",
        ("*", "More alignment settings"): "Plus de réglages d'alignement",
        ("*", "Show advanced alignment options"): "Afficher les options avancées d'alignement",
        ("*", "Segmentation"): "Segmentation",
        ("*", "Less..."): "Moins...",
        ("*", "Adjust"): "Ajuster",
        ("*", "Connections"): "Connexions",
        ("*", "Add connectors"): "Ajouter des connecteurs",
        ("Operator", "Add connectors"): "Ajouter des connecteurs",
        ("*", "Place connectors (click)"): "Placer des connecteurs (clic)",
        ("Operator", "Place connectors (click)"): "Placer des connecteurs (clic)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Choisir des faces en mode Objet (A = cible, B = mobile)",
        ("*", "A: none"): "A : aucune",
        ("*", "B: none"): "B : aucune",
        ("*", "Pick Face A"): "Choisir face A",
        ("Operator", "Pick Face A"): "Choisir face A",
        ("*", "Pick Face B"): "Choisir face B",
        ("Operator", "Pick Face B"): "Choisir face B",
        ("*", "Align Faces"): "Aligner les faces",
        ("Operator", "Align Faces"): "Aligner les faces",
    },
    "es": {
        ("*", "Adjust split axis"): "Ajustar eje de corte",
        ("Operator", "Adjust split axis"): "Ajustar eje de corte",
        ("*", "Split axis adjusted."): "Eje de corte ajustado.",
        ("*", "Adjust split axis cancelled."): "Ajuste del eje de corte cancelado.",
        ("*", "Planar Split"): "Corte planar",
        ("Operator", "Planar Split"): "Corte planar",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Dividir en muchas partes puede llevar tiempo en mallas densas...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "El cierre automático no encontró bucles válidos.",
        ("*", "Auto-capped seams on {n} part(s)."): "Cierres automáticos en {n} parte(s).",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Se crearon menos partes de las esperadas ({have} < {want}).",
        ("*", "{n} parts created."): "Se crearon {n} partes.",
        ("*", "Cap seams now"): "Cerrar bordes ahora",
        ("Operator", "Cap seams now"): "Cerrar bordes ahora",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Rellenar entre exactamente dos bucles de aristas de corte (externo+interno) por plano. Seeds preferidos.",
        ("*", "Only selected objects"): "Solo objetos seleccionados",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = todos los planes por objeto, 1 = solo el mayor",
        ("*", "Select only (no fill)"): "Solo seleccionar (sin rellenar)",
        ("*", "Require exactly two seed edges"): "Exigir exactamente dos aristas seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Si hay exactamente dos aristas seleccionadas en Modo Edición, usarlas como seeds únicamente (sin autodetección).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "No hay objetos de malla para cerrar. Seleccione piezas divididas o use la colección de piezas.",
        ("*", "Processing failed on '{name}': {err}"): "Error al procesar «{name}»: {err}",
        ("*", "Could not determine split edge loops to select."): "No se pudieron determinar los bucles de aristas de corte para seleccionar.",
        ("*", "Could not determine and fill split edge loops."): "No se pudieron determinar y rellenar los bucles de aristas de corte.",
        ("*", "Selected split edge loops on {n} object(s)."): "Bucles de aristas de corte seleccionados en {n} objeto(s).",
        ("*", "Capped seams on {n} object(s)."): "Bordes cerrados en {n} objeto(s).",
        ("*", "Please select a mesh object."): "Seleccione un objeto de malla.",
        ("*", "Object has unapplied transforms"): "El objeto tiene transformaciones no aplicadas",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Considere aplicar todas las transformaciones (Ctrl+A) para resultados precisos y predecibles.",
        ("*", "Split Offset (mm)"): "Desplazamiento de corte (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Desplazamiento del plano de corte a lo largo del eje (positivo en la dirección del eje)",
        ("*", "Split Axis"): "Eje de corte",
        ("*", "Split along X"): "Cortar a lo largo de X",
        ("*", "Split along Y"): "Cortar a lo largo de Y",
        ("*", "Split along Z"): "Cortar a lo largo de Z",
        ("*", "Show split preview"): "Mostrar vista previa de corte",
        ("*", "Show temporary orange planes at planned cut positions"): "Mostrar planos naranjas temporales en posiciones de corte previstas",
        ("*", "Number of Parts"): "Número de partes",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Número de segmentos deseados (planos de corte = partes - 1)",
        ("*", "Cap seams during split"): "Cerrar bordes durante el corte",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Cerrar automáticamente los bordes tras el corte. Con cavidad/carcasa interna: relleno preciso de los bucles externo/interno; sin cavidad: relleno simple. Puede aumentar el tiempo de ejecución.",
        ("*", "Connector Type"): "Tipo de conector",
        ("*", "Cylinder Pin"): "Pasador cilíndrico",
        ("*", "Dowel pin + socket"): "Pasador + casquillo",
        ("*", "Rectangular Tenon"): "Espiga rectangular",
        ("*", "Anti-rotation joint"): "Unión antirrotación",
        ("*", "Dovetail"): "Cola de milano",
        ("*", "Tapered wedge connector"): "Conector en cuña cónica",
        ("*", "Snap Pin"): "Pasador a presión",
        ("*", "Connector with snap spheres"): "Conector con esferas de enganche",
        ("*", "Snap Tenon"): "Espiga a presión",
        ("*", "Rectangular tenon with snap spheres"): "Espiga rectangular con esferas de enganche",
        ("*", "Snap Dovetail"): "Cola de milano a presión",
        ("*", "Tapered wedge connector with snap spheres"): "Conector en cuña cónica con esferas de enganche",
        ("*", "Custom Connector"): "Conector personalizado",
        ("*", "Use another mesh object from the scene as connector shape"): "Usar otro objeto de malla de la escena como forma de conector",
        ("*", "Select connector object"): "Seleccionar objeto conector",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Objeto de malla de esta escena usado como forma de conector. Su eje Z local se trata como dirección de inserción; se reescalará según los valores de Ancho/Longitud/Profundidad de abajo.",
        ("*", "Custom Width (mm)"): "Ancho personalizado (mm)",
        ("*", "Target size along the object's local X axis"): "Tamaño objetivo a lo largo del eje X local del objeto",
        ("*", "Custom Length (mm)"): "Longitud personalizada (mm)",
        ("*", "Target size along the object's local Y axis"): "Tamaño objetivo a lo largo del eje Y local del objeto",
        ("*", "Custom Depth (mm)"): "Profundidad personalizada (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Tamaño objetivo a lo largo del eje Z local del objeto (profundidad de inserción)",
        ("*", "Please select a connector object for Custom Connector."): "Seleccione un objeto conector para el Conector personalizado.",
        ("*", "Selected connector object has no usable mesh data."): "El objeto conector seleccionado no contiene datos de malla utilizables.",
        ("*", "Base size"): "Tamaño base",
        ("*", "Dovetail Width (mm)"): "Ancho de cola de milano (mm)",
        ("*", "Dovetail Length (mm)"): "Longitud de cola de milano (mm)",
        ("*", "Length along seam plane (local v)"): "Longitud a lo largo del plano de la junta (v local)",
        ("*", "Dovetail Depth (mm)"): "Profundidad de cola de milano (mm)",
        ("*", "Taper (%)"): "Conicidad (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Porcentaje en que la punta es más estrecha que la base",
        ("*", "Signed Taper (%)"): "Conicidad con signo (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Conicidad con signo a lo largo de la inserción. Positivo ensancha, negativo estrecha. Si es distinto de cero, sobrescribe la conicidad simple.",
        ("*", "Span Axis"): "Eje de extensión",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Auto estira a lo largo del eje de ancho de la cola de milano y recorta hacia los lados exteriores; X/Y/Z fuerzan un sobrepaso a lo largo de ese eje del mundo si se encuentra en el plano de la junta; Ninguno usa la longitud configurada manualmente",
        ("*", "None"): "Ninguno",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Usa la longitud de cola de milano configurada manualmente; solo recorta los bordes si el Corte de lado duro está activado",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Estira automáticamente a lo largo del eje de ancho de la cola de milano y recorta hacia los lados exteriores",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Fuerza el sobrepaso a lo largo del eje mundial X, si se encuentra en el plano de la junta",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Fuerza el sobrepaso a lo largo del eje mundial Y, si se encuentra en el plano de la junta",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Fuerza el sobrepaso a lo largo del eje mundial Z, si se encuentra en el plano de la junta",
        ("*", "Forces hard-side cut along this axis."): "Fuerza un corte de lado duro a lo largo de este eje.",
        ("*", "Hard-side Cut"): "Corte de lado duro",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Prefiere un corte lateral nítido para el encaje/ranura de cola de milano",
        ("*", "Margin (%)"): "Margen (%)",
        ("*", "Trim percentage at both ends of seam span"): "Porcentaje de recorte en ambos extremos de la extensión de la junta",
        ("*", "Placement"): "Colocación",
        ("*", "Offset along Width (mm)"): "Desplazamiento a lo largo del ancho (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Desplazamiento dentro del plano de corte a lo largo del eje de ancho (u) para desplazar el patrón de cola de milano",
        ("*", "Offset along Length (mm)"): "Desplazamiento a lo largo de la longitud (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Desplazamiento dentro del plano de corte a lo largo del eje de longitud (v) para desplazar el patrón de cola de milano",
        ("*", "Rotation in plane (deg)"): "Rotación en el plano (grados)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotación dentro del plano de corte para orientar el patrón de cola de milano",
        ("*", "Span Mode"): "Modo de extensión",
        ("*", "How the dovetail spans along the seam"): "Cómo se extiende la cola de milano a lo largo de la junta",
        ("*", "Auto"): "Automático",
        ("*", "Use full edge-to-edge span of the seam"): "Usar la extensión completa de borde a borde de la junta",
        ("*", "Fixed"): "Fijo",
        ("*", "Use a fixed repeating spacing"): "Usar un espaciado fijo repetido",
        ("*", "Centered"): "Centrado",
        ("*", "Center block(s) with margins"): "Centrar bloque(s) con márgenes",
        ("*", "Live Preview"): "Vista previa en vivo",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Muestra una vista previa en alambre en vivo de la colocación de conectores (Línea/Cuadrícula) para la selección actual. Limitado a 200 objetos de vista previa por rendimiento.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "La vista previa en vivo de conectores se detuvo en 200 objetos; los puntos restantes no se muestran.",
        ("*", "Distribution"): "Distribución",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Distribuir conectores a lo largo de una línea o en una cuadrícula sobre la superficie de la junta",
        ("*", "Line"): "Línea",
        ("*", "Place connectors along a line in the seam face"): "Colocar conectores a lo largo de una línea en la superficie de la junta",
        ("*", "Grid"): "Cuadrícula",
        ("*", "Distribute connectors in a grid over the seam face"): "Distribuir conectores en una cuadrícula sobre la superficie de la junta",
        ("*", "Connectors per Seam"): "Conectores por junta",
        ("*", "Rows (GRID)"): "Filas (CUADRÍCULA)",
        ("*", "Number of rows for grid distribution"): "Número de filas para la distribución en cuadrícula",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Margen del borde a lo largo de la junta (y perpendicular en CUADRÍCULA) como porcentaje de la longitud de la pieza (0–40 % recomendado)",
        ("*", "Spheres per side"): "Esferas por lado",
        ("*", "Number of snap spheres per side/around"): "Número de esferas de enganche por lado/alrededor",
        ("*", "Sphere Diameter (mm)"): "Diámetro de esfera (mm)",
        ("*", "Diameter of snap spheres"): "Diámetro de las esferas de enganche",
        ("*", "Protrusion (mm)"): "Protrusión (mm)",
        ("*", "How far spheres protrude from side surface"): "Cuánto sobresalen las esferas de la superficie lateral",
        ("*", "Pin Diameter (mm)"): "Diámetro del pasador (mm)",
        ("*", "Pin Length (mm)"): "Longitud del pasador (mm)",
        ("*", "Segments"): "Segmentos",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segmentos radiales del pasador cilíndrico (suavidad visual)",
        ("*", "Tenon Width (mm)"): "Ancho de la espiga (mm)",
        ("*", "Tenon Depth (mm)"): "Profundidad de la espiga (mm)",
        ("*", "Chamfer (mm)"): "Chaflán (mm)",
        ("*", "Insert Depth (%)"): "Profundidad de inserción (%)",
        ("*", "Percentage of connector length recessed into part A"): "Porcentaje de la longitud del conector empotrado en la pieza A",
        ("*", "Material Profiles"): "Perfiles de material",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Seleccione un perfil de material para rellenar automáticamente la tolerancia por lado",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Tolerancia recomendada por lado: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolerancia por cara (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Sobrescribe el perfil de material (0 = usar valor del perfil)",
        ("*", "More segmentation settings"): "Más ajustes de segmentación",
        ("*", "Show advanced segmentation options"): "Mostrar opciones avanzadas de segmentación",
        ("*", "More connection settings"): "Más ajustes de conexión",
        ("*", "Show advanced connection/geometry options"): "Mostrar opciones avanzadas de conexión/geometría",
        ("*", "More tolerance settings"): "Más ajustes de tolerancia",
        ("*", "Show advanced tolerance options"): "Mostrar opciones avanzadas de tolerancia",
        ("*", "More alignment settings"): "Más ajustes de alineación",
        ("*", "Show advanced alignment options"): "Mostrar opciones avanzadas de alineación",
        ("*", "Segmentation"): "Segmentación",
        ("*", "Less..."): "Menos...",
        ("*", "Adjust"): "Ajustar",
        ("*", "Connections"): "Conexiones",
        ("*", "Add connectors"): "Añadir conectores",
        ("Operator", "Add connectors"): "Añadir conectores",
        ("*", "Place connectors (click)"): "Colocar conectores (clic)",
        ("Operator", "Place connectors (click)"): "Colocar conectores (clic)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Elegir caras en Modo Objeto (A = objetivo, B = móvil)",
        ("*", "A: none"): "A: ninguno",
        ("*", "B: none"): "B: ninguno",
        ("*", "Pick Face A"): "Elegir Cara A",
        ("Operator", "Pick Face A"): "Elegir Cara A",
        ("*", "Pick Face B"): "Elegir Cara B",
        ("Operator", "Pick Face B"): "Elegir Cara B",
        ("*", "Align Faces"): "Alinear caras",
        ("Operator", "Align Faces"): "Alinear caras",
    },
    "it_IT": {
        ("*", "Adjust split axis"): "Regola asse di taglio",
        ("Operator", "Adjust split axis"): "Regola asse di taglio",
        ("*", "Split axis adjusted."): "Asse di taglio regolato.",
        ("*", "Adjust split axis cancelled."): "Regolazione dell'asse di taglio annullata.",
        ("*", "Planar Split"): "Taglio planare",
        ("Operator", "Planar Split"): "Taglio planare",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "La suddivisione in molte parti può richiedere tempo su mesh dense...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "La chiusura automatica non ha trovato loop validi.",
        ("*", "Auto-capped seams on {n} part(s)."): "Chiusure automatiche su {n} parte/i.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Create meno parti del previsto ({have} < {want}).",
        ("*", "{n} parts created."): "Create {n} parti.",
        ("*", "Cap seams now"): "Chiudi bordi ora",
        ("Operator", "Cap seams now"): "Chiudi bordi ora",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Riempi tra esattamente due loop di spigoli di taglio (esterno+interno) per piano. Seeds preferiti.",
        ("*", "Only selected objects"): "Solo oggetti selezionati",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = tutti i piani per oggetto, 1 = solo il maggiore",
        ("*", "Select only (no fill)"): "Solo seleziona (non riempire)",
        ("*", "Require exactly two seed edges"): "Richiedi esattamente due spigoli seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Se in Modalità Modifica sono selezionati esattamente due spigoli, usali solo come seeds (nessun rilevamento automatico).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Nessun oggetto mesh da chiudere. Seleziona parti divise o usa la collezione delle parti.",
        ("*", "Processing failed on '{name}': {err}"): "Elaborazione non riuscita su «{name}»: {err}",
        ("*", "Could not determine split edge loops to select."): "Impossibile determinare i loop di spigoli di taglio da selezionare.",
        ("*", "Could not determine and fill split edge loops."): "Impossibile determinare e riempire i loop di spigoli di taglio.",
        ("*", "Selected split edge loops on {n} object(s)."): "Loop di spigoli di taglio selezionati su {n} oggetto/i.",
        ("*", "Capped seams on {n} object(s)."): "Bordi chiusi su {n} oggetto/i.",
        ("*", "Please select a mesh object."): "Seleziona un oggetto mesh.",
        ("*", "Object has unapplied transforms"): "L'oggetto ha trasformazioni non applicate",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Valuta di applicare tutte le trasformazioni (Ctrl+A) per risultati precisi e prevedibili.",
        ("*", "Split Offset (mm)"): "Offset di taglio (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Offset del piano di taglio lungo l'asse (positivo nella direzione dell'asse)",
        ("*", "Split Axis"): "Asse di taglio",
        ("*", "Split along X"): "Taglia lungo X",
        ("*", "Split along Y"): "Taglia lungo Y",
        ("*", "Split along Z"): "Taglia lungo Z",
        ("*", "Show split preview"): "Mostra anteprima taglio",
        ("*", "Show temporary orange planes at planned cut positions"): "Mostra piani arancioni temporanei nelle posizioni di taglio previste",
        ("*", "Number of Parts"): "Numero di parti",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Numero di segmenti desiderati (piani di taglio = parti - 1)",
        ("*", "Cap seams during split"): "Chiudi bordi durante il taglio",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Chiudi automaticamente i bordi dopo il taglio. Con cavità/guscio interno: riempimento preciso dei loop esterno/interno; senza cavità: riempimento semplice. Può aumentare i tempi.",
        ("*", "Connector Type"): "Tipo di connettore",
        ("*", "Cylinder Pin"): "Perno cilindrico",
        ("*", "Dowel pin + socket"): "Perno + boccola",
        ("*", "Rectangular Tenon"): "Tenone rettangolare",
        ("*", "Anti-rotation joint"): "Giunto anti-rotazione",
        ("*", "Dovetail"): "Coda di rondine",
        ("*", "Tapered wedge connector"): "Connettore a cuneo conico",
        ("*", "Snap Pin"): "Perno a scatto",
        ("*", "Connector with snap spheres"): "Connettore con sfere a scatto",
        ("*", "Snap Tenon"): "Tenone a scatto",
        ("*", "Rectangular tenon with snap spheres"): "Tenone rettangolare con sfere a scatto",
        ("*", "Snap Dovetail"): "Coda di rondine a scatto",
        ("*", "Tapered wedge connector with snap spheres"): "Connettore a cuneo conico con sfere a scatto",
        ("*", "Custom Connector"): "Connettore personalizzato",
        ("*", "Use another mesh object from the scene as connector shape"): "Usa un altro oggetto mesh della scena come forma del connettore",
        ("*", "Select connector object"): "Seleziona oggetto connettore",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Oggetto mesh di questa scena usato come forma del connettore. Il suo asse Z locale è trattato come direzione di inserimento; verrà ridimensionato secondo i valori di Larghezza/Lunghezza/Profondità sottostanti.",
        ("*", "Custom Width (mm)"): "Larghezza personalizzata (mm)",
        ("*", "Target size along the object's local X axis"): "Dimensione target lungo l'asse X locale dell'oggetto",
        ("*", "Custom Length (mm)"): "Lunghezza personalizzata (mm)",
        ("*", "Target size along the object's local Y axis"): "Dimensione target lungo l'asse Y locale dell'oggetto",
        ("*", "Custom Depth (mm)"): "Profondità personalizzata (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Dimensione target lungo l'asse Z locale dell'oggetto (profondità di inserimento)",
        ("*", "Please select a connector object for Custom Connector."): "Seleziona un oggetto connettore per il Connettore personalizzato.",
        ("*", "Selected connector object has no usable mesh data."): "L'oggetto connettore selezionato non contiene dati mesh utilizzabili.",
        ("*", "Base size"): "Dimensione base",
        ("*", "Dovetail Width (mm)"): "Larghezza coda di rondine (mm)",
        ("*", "Dovetail Length (mm)"): "Lunghezza coda di rondine (mm)",
        ("*", "Length along seam plane (local v)"): "Lunghezza lungo il piano della giunzione (v locale)",
        ("*", "Dovetail Depth (mm)"): "Profondità coda di rondine (mm)",
        ("*", "Taper (%)"): "Rastremazione (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Percentuale di quanto la punta è più stretta della base",
        ("*", "Signed Taper (%)"): "Rastremazione con segno (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Rastremazione con segno lungo l'inserimento. Positivo allarga, negativo restringe. Se diverso da zero, sostituisce la rastremazione semplice.",
        ("*", "Span Axis"): "Asse di estensione",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Auto si estende lungo l'asse di larghezza della coda di rondine e taglia verso i lati esterni; X/Y/Z forzano uno sconfinamento lungo quell'asse mondiale se giace nel piano della giunzione; Nessuno usa la lunghezza configurata manualmente",
        ("*", "None"): "Nessuno",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Usa la lunghezza della coda di rondine configurata manualmente; taglia i bordi solo se il Taglio a lato duro è attivo",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Estende automaticamente lungo l'asse di larghezza della coda di rondine e taglia verso i lati esterni",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Forza lo sconfinamento lungo l'asse mondiale X, se giace nel piano della giunzione",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Forza lo sconfinamento lungo l'asse mondiale Y, se giace nel piano della giunzione",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Forza lo sconfinamento lungo l'asse mondiale Z, se giace nel piano della giunzione",
        ("*", "Forces hard-side cut along this axis."): "Forza un taglio a lato duro lungo questo asse.",
        ("*", "Hard-side Cut"): "Taglio a lato duro",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Preferisce un taglio laterale netto per l'incastro/scanalatura a coda di rondine",
        ("*", "Margin (%)"): "Margine (%)",
        ("*", "Trim percentage at both ends of seam span"): "Percentuale di rifilatura a entrambe le estremità dell'estensione della giunzione",
        ("*", "Placement"): "Posizionamento",
        ("*", "Offset along Width (mm)"): "Offset lungo la larghezza (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Offset all'interno del piano di taglio lungo l'asse di larghezza (u) per spostare il pattern a coda di rondine",
        ("*", "Offset along Length (mm)"): "Offset lungo la lunghezza (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Offset all'interno del piano di taglio lungo l'asse di lunghezza (v) per spostare il pattern a coda di rondine",
        ("*", "Rotation in plane (deg)"): "Rotazione nel piano (gradi)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotazione all'interno del piano di taglio per orientare il pattern a coda di rondine",
        ("*", "Span Mode"): "Modalità di estensione",
        ("*", "How the dovetail spans along the seam"): "Come la coda di rondine si estende lungo la giunzione",
        ("*", "Auto"): "Automatico",
        ("*", "Use full edge-to-edge span of the seam"): "Usa l'estensione completa da bordo a bordo della giunzione",
        ("*", "Fixed"): "Fisso",
        ("*", "Use a fixed repeating spacing"): "Usa una spaziatura fissa ripetuta",
        ("*", "Centered"): "Centrato",
        ("*", "Center block(s) with margins"): "Centra il/i blocco/i con margini",
        ("*", "Live Preview"): "Anteprima dal vivo",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Mostra un'anteprima wireframe dal vivo del posizionamento dei connettori (Linea/Griglia) per la selezione corrente. Limitata a 200 oggetti di anteprima per motivi di prestazioni.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "L'anteprima dal vivo dei connettori si è fermata a 200 oggetti; i punti restanti non vengono mostrati.",
        ("*", "Distribution"): "Distribuzione",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Distribuisci i connettori lungo una linea o in una griglia sulla superficie della giunzione",
        ("*", "Line"): "Linea",
        ("*", "Place connectors along a line in the seam face"): "Posiziona i connettori lungo una linea sulla superficie della giunzione",
        ("*", "Grid"): "Griglia",
        ("*", "Distribute connectors in a grid over the seam face"): "Distribuisci i connettori in una griglia sulla superficie della giunzione",
        ("*", "Connectors per Seam"): "Connettori per giunzione",
        ("*", "Rows (GRID)"): "Righe (GRIGLIA)",
        ("*", "Number of rows for grid distribution"): "Numero di righe per la distribuzione a griglia",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Margine del bordo lungo la giunzione (e perpendicolare in GRIGLIA) come percentuale della lunghezza del pezzo (0–40% consigliato)",
        ("*", "Spheres per side"): "Sfere per lato",
        ("*", "Number of snap spheres per side/around"): "Numero di sfere a scatto per lato/intorno",
        ("*", "Sphere Diameter (mm)"): "Diametro sfera (mm)",
        ("*", "Diameter of snap spheres"): "Diametro delle sfere a scatto",
        ("*", "Protrusion (mm)"): "Sporgenza (mm)",
        ("*", "How far spheres protrude from side surface"): "Entità di sporgenza delle sfere dalla superficie laterale",
        ("*", "Pin Diameter (mm)"): "Diametro del perno (mm)",
        ("*", "Pin Length (mm)"): "Lunghezza del perno (mm)",
        ("*", "Segments"): "Segmenti",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segmenti radiali del perno cilindrico (morbidezza visiva)",
        ("*", "Tenon Width (mm)"): "Larghezza del tenone (mm)",
        ("*", "Tenon Depth (mm)"): "Profondità del tenone (mm)",
        ("*", "Chamfer (mm)"): "Smusso (mm)",
        ("*", "Insert Depth (%)"): "Profondità di inserimento (%)",
        ("*", "Percentage of connector length recessed into part A"): "Percentuale della lunghezza del connettore incassata nella parte A",
        ("*", "Material Profiles"): "Profili materiale",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Seleziona un profilo materiale per precompilare la tolleranza per lato",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Tolleranza consigliata per lato: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolleranza per faccia (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Sovrascrive il profilo materiale (0 = usa valore del profilo)",
        ("*", "More segmentation settings"): "Altre impostazioni di segmentazione",
        ("*", "Show advanced segmentation options"): "Mostra le opzioni avanzate di segmentazione",
        ("*", "More connection settings"): "Altre impostazioni di connessione",
        ("*", "Show advanced connection/geometry options"): "Mostra le opzioni avanzate di connessione/geometria",
        ("*", "More tolerance settings"): "Altre impostazioni di tolleranza",
        ("*", "Show advanced tolerance options"): "Mostra le opzioni avanzate di tolleranza",
        ("*", "More alignment settings"): "Altre impostazioni di allineamento",
        ("*", "Show advanced alignment options"): "Mostra le opzioni avanzate di allineamento",
        ("*", "Segmentation"): "Segmentazione",
        ("*", "Less..."): "Meno...",
        ("*", "Adjust"): "Regola",
        ("*", "Connections"): "Connessioni",
        ("*", "Add connectors"): "Aggiungi connettori",
        ("Operator", "Add connectors"): "Aggiungi connettori",
        ("*", "Place connectors (click)"): "Posiziona connettori (clic)",
        ("Operator", "Place connectors (click)"): "Posiziona connettori (clic)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Scegli facce in Modalità Oggetto (A = bersaglio, B = mobile)",
        ("*", "A: none"): "A: nessuna",
        ("*", "B: none"): "B: nessuna",
        ("*", "Pick Face A"): "Scegli Faccia A",
        ("Operator", "Pick Face A"): "Scegli Faccia A",
        ("*", "Pick Face B"): "Scegli Faccia B",
        ("Operator", "Pick Face B"): "Scegli Faccia B",
        ("*", "Align Faces"): "Allinea facce",
        ("Operator", "Align Faces"): "Allinea facce",
    },
    "pt_BR": {
        ("*", "Adjust split axis"): "Ajustar eixo de corte",
        ("Operator", "Adjust split axis"): "Ajustar eixo de corte",
        ("*", "Split axis adjusted."): "Eixo de corte ajustado.",
        ("*", "Adjust split axis cancelled."): "Ajuste do eixo de corte cancelado.",
        ("*", "Planar Split"): "Corte planar",
        ("Operator", "Planar Split"): "Corte planar",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Dividir em muitas partes pode levar tempo em malhas densas...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "O fechamento automático não encontrou loops válidos.",
        ("*", "Auto-capped seams on {n} part(s)."): "Fechamentos automáticos em {n} parte(s).",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Menos partes criadas do que o esperado ({have} < {want}).",
        ("*", "{n} parts created."): "{n} partes criadas.",
        ("*", "Cap seams now"): "Fechar bordas agora",
        ("Operator", "Cap seams now"): "Fechar bordas agora",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Preencher entre exatamente dois loops de arestas de corte (externo+interno) por plano. Seeds preferidos.",
        ("*", "Only selected objects"): "Apenas objetos selecionados",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = todos os planos por objeto, 1 = apenas o maior",
        ("*", "Select only (no fill)"): "Apenas selecionar (sem preencher)",
        ("*", "Require exactly two seed edges"): "Exigir exatamente duas arestas seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Se exatamente duas arestas estiverem selecionadas no Modo de Edição, usá-las apenas como seeds (sem detecção automática).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Nenhum objeto de malha para fechar. Selecione partes divididas ou use a coleção de partes.",
        ("*", "Processing failed on '{name}': {err}"): "Falha ao processar «{name}»: {err}",
        ("*", "Could not determine split edge loops to select."): "Não foi possível determinar os loops de arestas de corte para selecionar.",
        ("*", "Could not determine and fill split edge loops."): "Não foi possível determinar e preencher os loops de arestas de corte.",
        ("*", "Selected split edge loops on {n} object(s)."): "Loops de arestas de corte selecionados em {n} objeto(s).",
        ("*", "Capped seams on {n} object(s)."): "Bordas fechadas em {n} objeto(s).",
        ("*", "Please select a mesh object."): "Selecione um objeto de malha.",
        ("*", "Object has unapplied transforms"): "O objeto possui transformações não aplicadas",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Considere aplicar todas as transformações (Ctrl+A) para resultados precisos e previsíveis.",
        ("*", "Split Offset (mm)"): "Deslocamento de corte (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Deslocamento do plano de corte ao longo do eixo (positivo na direção do eixo)",
        ("*", "Split Axis"): "Eixo de corte",
        ("*", "Split along X"): "Cortar ao longo de X",
        ("*", "Split along Y"): "Cortar ao longo de Y",
        ("*", "Split along Z"): "Cortar ao longo de Z",
        ("*", "Show split preview"): "Mostrar prévia de corte",
        ("*", "Show temporary orange planes at planned cut positions"): "Mostrar planos laranja temporários nas posições de corte previstas",
        ("*", "Number of Parts"): "Número de partes",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Número de segmentos desejados (planos de corte = partes - 1)",
        ("*", "Cap seams during split"): "Fechar bordas durante o corte",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Fechar automaticamente as bordas após o corte. Com cavidade/casca interna: preenchimento preciso dos loops externo/interno; sem cavidade: preenchimento simples. Pode aumentar o tempo de execução.",
        ("*", "Connector Type"): "Tipo de conector",
        ("*", "Cylinder Pin"): "Pino cilíndrico",
        ("*", "Dowel pin + socket"): "Pino + bucha",
        ("*", "Rectangular Tenon"): "Espiga retangular",
        ("*", "Anti-rotation joint"): "Junção anti-rotação",
        ("*", "Dovetail"): "Rabo de andorinha",
        ("*", "Tapered wedge connector"): "Conector em cunha cônica",
        ("*", "Snap Pin"): "Pino de encaixe",
        ("*", "Connector with snap spheres"): "Conector com esferas de encaixe",
        ("*", "Snap Tenon"): "Espiga de encaixe",
        ("*", "Rectangular tenon with snap spheres"): "Espiga retangular com esferas de encaixe",
        ("*", "Snap Dovetail"): "Rabo de andorinha de encaixe",
        ("*", "Tapered wedge connector with snap spheres"): "Conector em cunha cônica com esferas de encaixe",
        ("*", "Custom Connector"): "Conector personalizado",
        ("*", "Use another mesh object from the scene as connector shape"): "Usar outro objeto de malha da cena como forma do conector",
        ("*", "Select connector object"): "Selecionar objeto conector",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Objeto de malha desta cena usado como forma do conector. Seu eixo Z local é tratado como direção de inserção; será redimensionado conforme os valores de Largura/Comprimento/Profundidade abaixo.",
        ("*", "Custom Width (mm)"): "Largura personalizada (mm)",
        ("*", "Target size along the object's local X axis"): "Tamanho alvo ao longo do eixo X local do objeto",
        ("*", "Custom Length (mm)"): "Comprimento personalizado (mm)",
        ("*", "Target size along the object's local Y axis"): "Tamanho alvo ao longo do eixo Y local do objeto",
        ("*", "Custom Depth (mm)"): "Profundidade personalizada (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Tamanho alvo ao longo do eixo Z local do objeto (profundidade de inserção)",
        ("*", "Please select a connector object for Custom Connector."): "Selecione um objeto conector para o Conector personalizado.",
        ("*", "Selected connector object has no usable mesh data."): "O objeto conector selecionado não contém dados de malha utilizáveis.",
        ("*", "Base size"): "Tamanho base",
        ("*", "Dovetail Width (mm)"): "Largura do rabo de andorinha (mm)",
        ("*", "Dovetail Length (mm)"): "Comprimento do rabo de andorinha (mm)",
        ("*", "Length along seam plane (local v)"): "Comprimento ao longo do plano da junta (v local)",
        ("*", "Dovetail Depth (mm)"): "Profundidade do rabo de andorinha (mm)",
        ("*", "Taper (%)"): "Afunilamento (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Percentual em que a ponta é mais estreita que a base",
        ("*", "Signed Taper (%)"): "Afunilamento com sinal (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Afunilamento com sinal ao longo da inserção. Positivo alarga, negativo estreita. Se diferente de zero, substitui o afunilamento simples.",
        ("*", "Span Axis"): "Eixo de extensão",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Auto estica ao longo do eixo de largura do rabo de andorinha e apara em direção às laterais externas; X/Y/Z forçam um transbordo ao longo desse eixo do mundo se estiver no plano da junta; Nenhum usa o comprimento configurado manualmente",
        ("*", "None"): "Nenhum",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Usa o comprimento do rabo de andorinha configurado manualmente; apara as bordas apenas se o Corte de lado rígido estiver ativado",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Estica automaticamente ao longo do eixo de largura do rabo de andorinha e apara em direção às laterais externas",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Força o transbordo ao longo do eixo mundial X, se estiver no plano da junta",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Força o transbordo ao longo do eixo mundial Y, se estiver no plano da junta",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Força o transbordo ao longo do eixo mundial Z, se estiver no plano da junta",
        ("*", "Forces hard-side cut along this axis."): "Força um corte de lado rígido ao longo deste eixo.",
        ("*", "Hard-side Cut"): "Corte de lado rígido",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Prefere um corte lateral nítido para o encaixe/ranhura do rabo de andorinha",
        ("*", "Margin (%)"): "Margem (%)",
        ("*", "Trim percentage at both ends of seam span"): "Percentual de corte em ambas as extremidades da extensão da junta",
        ("*", "Placement"): "Posicionamento",
        ("*", "Offset along Width (mm)"): "Deslocamento ao longo da largura (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Deslocamento dentro do plano de corte ao longo do eixo de largura (u) para deslocar o padrão do rabo de andorinha",
        ("*", "Offset along Length (mm)"): "Deslocamento ao longo do comprimento (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Deslocamento dentro do plano de corte ao longo do eixo de comprimento (v) para deslocar o padrão do rabo de andorinha",
        ("*", "Rotation in plane (deg)"): "Rotação no plano (graus)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotação dentro do plano de corte para orientar o padrão do rabo de andorinha",
        ("*", "Span Mode"): "Modo de extensão",
        ("*", "How the dovetail spans along the seam"): "Como o rabo de andorinha se estende ao longo da junta",
        ("*", "Auto"): "Automático",
        ("*", "Use full edge-to-edge span of the seam"): "Usar a extensão completa de borda a borda da junta",
        ("*", "Fixed"): "Fixo",
        ("*", "Use a fixed repeating spacing"): "Usar um espaçamento fixo repetido",
        ("*", "Centered"): "Centralizado",
        ("*", "Center block(s) with margins"): "Centralizar bloco(s) com margens",
        ("*", "Live Preview"): "Pré-visualização ao vivo",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Mostra uma pré-visualização em wireframe, em tempo real, do posicionamento dos conectores (Linha/Grade) para a seleção atual. Limitada a 200 objetos de pré-visualização por desempenho.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "A pré-visualização ao vivo dos conectores parou em 200 objetos; os pontos restantes não são exibidos.",
        ("*", "Distribution"): "Distribuição",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Distribua conectores ao longo de uma linha ou em uma grade na superfície da junta",
        ("*", "Line"): "Linha",
        ("*", "Place connectors along a line in the seam face"): "Coloque conectores ao longo de uma linha na superfície da junta",
        ("*", "Grid"): "Grade",
        ("*", "Distribute connectors in a grid over the seam face"): "Distribua conectores em uma grade na superfície da junta",
        ("*", "Connectors per Seam"): "Conectores por junta",
        ("*", "Rows (GRID)"): "Linhas (GRADE)",
        ("*", "Number of rows for grid distribution"): "Número de linhas para a distribuição em grade",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Margem da borda ao longo da junta (e perpendicular na GRADE) como porcentagem do comprimento da peça (0–40% recomendado)",
        ("*", "Spheres per side"): "Esferas por lado",
        ("*", "Number of snap spheres per side/around"): "Número de esferas de encaixe por lado/ao redor",
        ("*", "Sphere Diameter (mm)"): "Diâmetro da esfera (mm)",
        ("*", "Diameter of snap spheres"): "Diâmetro das esferas de encaixe",
        ("*", "Protrusion (mm)"): "Saliente (mm)",
        ("*", "How far spheres protrude from side surface"): "O quanto as esferas se projetam da superfície lateral",
        ("*", "Pin Diameter (mm)"): "Diâmetro do pino (mm)",
        ("*", "Pin Length (mm)"): "Comprimento do pino (mm)",
        ("*", "Segments"): "Segmentos",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segmentos radiais do pino cilíndrico (suavidade visual)",
        ("*", "Tenon Width (mm)"): "Largura da espiga (mm)",
        ("*", "Tenon Depth (mm)"): "Profundidade da espiga (mm)",
        ("*", "Chamfer (mm)"): "Chanfro (mm)",
        ("*", "Insert Depth (%)"): "Profundidade de inserção (%)",
        ("*", "Percentage of connector length recessed into part A"): "Percentual do comprimento do conector embutido na peça A",
        ("*", "Material Profiles"): "Perfis de material",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Selecione um perfil de material para preencher automaticamente a tolerância por lado",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Tolerância recomendada por lado: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolerância por face (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Substitui o perfil de material (0 = usar valor do perfil)",
        ("*", "More segmentation settings"): "Mais configurações de segmentação",
        ("*", "Show advanced segmentation options"): "Mostrar opções avançadas de segmentação",
        ("*", "More connection settings"): "Mais configurações de conexão",
        ("*", "Show advanced connection/geometry options"): "Mostrar opções avançadas de conexão/geometria",
        ("*", "More tolerance settings"): "Mais configurações de tolerância",
        ("*", "Show advanced tolerance options"): "Mostrar opções avançadas de tolerância",
        ("*", "More alignment settings"): "Mais configurações de alinhamento",
        ("*", "Show advanced alignment options"): "Mostrar opções avançadas de alinhamento",
        ("*", "Segmentation"): "Segmentação",
        ("*", "Less..."): "Menos...",
        ("*", "Adjust"): "Ajustar",
        ("*", "Connections"): "Conexões",
        ("*", "Add connectors"): "Adicionar conectores",
        ("Operator", "Add connectors"): "Adicionar conectores",
        ("*", "Place connectors (click)"): "Posicionar conectores (clique)",
        ("Operator", "Place connectors (click)"): "Posicionar conectores (clique)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Escolher faces no modo Objeto (A = alvo, B = móvel)",
        ("*", "A: none"): "A: nenhum",
        ("*", "B: none"): "B: nenhum",
        ("*", "Pick Face A"): "Escolher Face A",
        ("Operator", "Pick Face A"): "Escolher Face A",
        ("*", "Pick Face B"): "Escolher Face B",
        ("Operator", "Pick Face B"): "Escolher Face B",
        ("*", "Align Faces"): "Alinhar faces",
        ("Operator", "Align Faces"): "Alinhar faces",
    },
    "pt_PT": {
        ("*", "Adjust split axis"): "Ajustar eixo de corte",
        ("Operator", "Adjust split axis"): "Ajustar eixo de corte",
        ("*", "Split axis adjusted."): "Eixo de corte ajustado.",
        ("*", "Adjust split axis cancelled."): "Ajuste do eixo de corte cancelado.",
        ("*", "Planar Split"): "Corte planar",
        ("Operator", "Planar Split"): "Corte planar",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Dividir em muitas partes pode demorar em malhas densas...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "O fecho automático não encontrou loops válidos.",
        ("*", "Auto-capped seams on {n} part(s)."): "Fechos automáticos em {n} parte(s).",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Menos partes criadas do que o esperado ({have} < {want}).",
        ("*", "{n} parts created."): "{n} partes criadas.",
        ("*", "Cap seams now"): "Fechar arestas agora",
        ("Operator", "Cap seams now"): "Fechar arestas agora",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Preencher entre exatamente dois loops de arestas de corte (externo+interno) por plano. Seeds preferidos.",
        ("*", "Only selected objects"): "Apenas objetos selecionados",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = todos os planos por objeto, 1 = apenas o maior",
        ("*", "Select only (no fill)"): "Apenas selecionar (sem preencher)",
        ("*", "Require exactly two seed edges"): "Exigir exatamente duas arestas seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Se exatamente duas arestas estiverem selecionadas no Modo de Edição, usá-las apenas como seeds (sem deteção automática).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Nenhum objeto de malha para fechar. Selecione partes divididas ou utilize a coleção de partes.",
        ("*", "Processing failed on '{name}': {err}"): "Falha ao processar «{name}»: {err}",
        ("*", "Could not determine split edge loops to select."): "Não foi possível determinar os loops de arestas de corte para selecionar.",
        ("*", "Could not determine and fill split edge loops."): "Não foi possível determinar e preencher os loops de arestas de corte.",
        ("*", "Selected split edge loops on {n} object(s)."): "Loops de arestas de corte selecionados em {n} objeto(s).",
        ("*", "Capped seams on {n} object(s)."): "Arestas fechadas em {n} objeto(s).",
        ("*", "Please select a mesh object."): "Selecione um objeto de malha.",
        ("*", "Object has unapplied transforms"): "O objeto tem transformações não aplicadas",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Considere aplicar todas as transformações (Ctrl+A) para resultados precisos e previsíveis.",
        ("*", "Split Offset (mm)"): "Deslocamento de corte (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Deslocamento do plano de corte ao longo do eixo (positivo na direção do eixo)",
        ("*", "Split Axis"): "Eixo de corte",
        ("*", "Split along X"): "Cortar ao longo de X",
        ("*", "Split along Y"): "Cortar ao longo de Y",
        ("*", "Split along Z"): "Cortar ao longo de Z",
        ("*", "Show split preview"): "Mostrar pré-visualização do corte",
        ("*", "Show temporary orange planes at planned cut positions"): "Mostrar planos laranja temporários nas posições de corte previstas",
        ("*", "Number of Parts"): "Número de partes",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Número de segmentos desejados (planos de corte = partes - 1)",
        ("*", "Cap seams during split"): "Fechar arestas durante o corte",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Fechar automaticamente as arestas após o corte. Com cavidade/revestimento interno: enchimento preciso dos loops externo/interno; sem cavidade: enchimento simples. Pode aumentar o tempo de execução.",
        ("*", "Connector Type"): "Tipo de conector",
        ("*", "Cylinder Pin"): "Pino cilíndrico",
        ("*", "Dowel pin + socket"): "Pino + bucha",
        ("*", "Rectangular Tenon"): "Espiga retangular",
        ("*", "Anti-rotation joint"): "União anti-rotação",
        ("*", "Dovetail"): "Cauda de andorinha",
        ("*", "Tapered wedge connector"): "Conector em cunha cónica",
        ("*", "Snap Pin"): "Pino de encaixe",
        ("*", "Connector with snap spheres"): "Conector com esferas de encaixe",
        ("*", "Snap Tenon"): "Espiga de encaixe",
        ("*", "Rectangular tenon with snap spheres"): "Espiga retangular com esferas de encaixe",
        ("*", "Snap Dovetail"): "Cauda de andorinha de encaixe",
        ("*", "Tapered wedge connector with snap spheres"): "Conector em cunha cónica com esferas de encaixe",
        ("*", "Custom Connector"): "Conector personalizado",
        ("*", "Use another mesh object from the scene as connector shape"): "Utilizar outro objeto de malha da cena como forma do conector",
        ("*", "Select connector object"): "Selecionar objeto conector",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Objeto de malha desta cena utilizado como forma do conector. O seu eixo Z local é tratado como direção de inserção; será redimensionado de acordo com os valores de Largura/Comprimento/Profundidade abaixo.",
        ("*", "Custom Width (mm)"): "Largura personalizada (mm)",
        ("*", "Target size along the object's local X axis"): "Tamanho alvo ao longo do eixo X local do objeto",
        ("*", "Custom Length (mm)"): "Comprimento personalizado (mm)",
        ("*", "Target size along the object's local Y axis"): "Tamanho alvo ao longo do eixo Y local do objeto",
        ("*", "Custom Depth (mm)"): "Profundidade personalizada (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Tamanho alvo ao longo do eixo Z local do objeto (profundidade de inserção)",
        ("*", "Please select a connector object for Custom Connector."): "Selecione um objeto conector para o Conector personalizado.",
        ("*", "Selected connector object has no usable mesh data."): "O objeto conector selecionado não contém dados de malha utilizáveis.",
        ("*", "Base size"): "Tamanho base",
        ("*", "Dovetail Width (mm)"): "Largura da cauda de andorinha (mm)",
        ("*", "Dovetail Length (mm)"): "Comprimento da cauda de andorinha (mm)",
        ("*", "Length along seam plane (local v)"): "Comprimento ao longo do plano da junta (v local)",
        ("*", "Dovetail Depth (mm)"): "Profundidade da cauda de andorinha (mm)",
        ("*", "Taper (%)"): "Afunilamento (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Percentagem em que a ponta é mais estreita do que a base",
        ("*", "Signed Taper (%)"): "Afunilamento com sinal (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Afunilamento com sinal ao longo da inserção. Positivo alarga, negativo estreita. Se diferente de zero, substitui o afunilamento simples.",
        ("*", "Span Axis"): "Eixo de extensão",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Automático estica ao longo do eixo de largura da cauda de andorinha e corta em direção aos lados exteriores; X/Y/Z forçam um prolongamento ao longo desse eixo do mundo se estiver no plano da junta; Nenhum utiliza o comprimento configurado manualmente",
        ("*", "None"): "Nenhum",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Utiliza o comprimento da cauda de andorinha configurado manualmente; corta as bordas apenas se o Corte de lado rígido estiver ativo",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Estica automaticamente ao longo do eixo de largura da cauda de andorinha e corta em direção aos lados exteriores",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Força o prolongamento ao longo do eixo mundial X, se estiver no plano da junta",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Força o prolongamento ao longo do eixo mundial Y, se estiver no plano da junta",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Força o prolongamento ao longo do eixo mundial Z, se estiver no plano da junta",
        ("*", "Forces hard-side cut along this axis."): "Força um corte de lado rígido ao longo deste eixo.",
        ("*", "Hard-side Cut"): "Corte de lado rígido",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Prefere um corte lateral nítido para o encaixe/ranhura da cauda de andorinha",
        ("*", "Margin (%)"): "Margem (%)",
        ("*", "Trim percentage at both ends of seam span"): "Percentagem de corte em ambas as extremidades da extensão da junta",
        ("*", "Placement"): "Posicionamento",
        ("*", "Offset along Width (mm)"): "Deslocamento ao longo da largura (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Deslocamento dentro do plano de corte ao longo do eixo de largura (u) para deslocar o padrão da cauda de andorinha",
        ("*", "Offset along Length (mm)"): "Deslocamento ao longo do comprimento (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Deslocamento dentro do plano de corte ao longo do eixo de comprimento (v) para deslocar o padrão da cauda de andorinha",
        ("*", "Rotation in plane (deg)"): "Rotação no plano (graus)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotação dentro do plano de corte para orientar o padrão da cauda de andorinha",
        ("*", "Span Mode"): "Modo de extensão",
        ("*", "How the dovetail spans along the seam"): "Como a cauda de andorinha se estende ao longo da junta",
        ("*", "Auto"): "Automático",
        ("*", "Use full edge-to-edge span of the seam"): "Utilizar a extensão completa de borda a borda da junta",
        ("*", "Fixed"): "Fixo",
        ("*", "Use a fixed repeating spacing"): "Utilizar um espaçamento fixo repetido",
        ("*", "Centered"): "Centrado",
        ("*", "Center block(s) with margins"): "Centrar bloco(s) com margens",
        ("*", "Live Preview"): "Pré-visualização em tempo real",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Mostra uma pré-visualização em wireframe, em tempo real, do posicionamento dos conectores (Linha/Grelha) para a seleção atual. Limitada a 200 objetos de pré-visualização por motivos de desempenho.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "A pré-visualização em tempo real dos conectores parou nos 200 objetos; os pontos restantes não são apresentados.",
        ("*", "Distribution"): "Distribuição",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Distribuir conectores ao longo de uma linha ou numa grelha sobre a superfície da junta",
        ("*", "Line"): "Linha",
        ("*", "Place connectors along a line in the seam face"): "Colocar conectores ao longo de uma linha na superfície da junta",
        ("*", "Grid"): "Grelha",
        ("*", "Distribute connectors in a grid over the seam face"): "Distribuir conectores numa grelha sobre a superfície da junta",
        ("*", "Connectors per Seam"): "Conectores por junta",
        ("*", "Rows (GRID)"): "Linhas (GRELHA)",
        ("*", "Number of rows for grid distribution"): "Número de linhas para a distribuição em grelha",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Margem da aresta ao longo da junta (e perpendicular na GRELHA) como percentagem do comprimento da peça (0–40 % recomendado)",
        ("*", "Spheres per side"): "Esferas por lado",
        ("*", "Number of snap spheres per side/around"): "Número de esferas de encaixe por lado/à volta",
        ("*", "Sphere Diameter (mm)"): "Diâmetro da esfera (mm)",
        ("*", "Diameter of snap spheres"): "Diâmetro das esferas de encaixe",
        ("*", "Protrusion (mm)"): "Saliente (mm)",
        ("*", "How far spheres protrude from side surface"): "Quanto as esferas sobressaem da superfície lateral",
        ("*", "Pin Diameter (mm)"): "Diâmetro do pino (mm)",
        ("*", "Pin Length (mm)"): "Comprimento do pino (mm)",
        ("*", "Segments"): "Segmentos",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segmentos radiais do pino cilíndrico (suavidade visual)",
        ("*", "Tenon Width (mm)"): "Largura da espiga (mm)",
        ("*", "Tenon Depth (mm)"): "Profundidade da espiga (mm)",
        ("*", "Chamfer (mm)"): "Chanfro (mm)",
        ("*", "Insert Depth (%)"): "Profundidade de inserção (%)",
        ("*", "Percentage of connector length recessed into part A"): "Percentagem do comprimento do conector embutido na peça A",
        ("*", "Material Profiles"): "Perfis de material",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Selecione um perfil de material para preencher automaticamente a tolerância por lado",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Tolerância recomendada por lado: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolerância por face (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Substitui o perfil de material (0 = utilizar valor do perfil)",
        ("*", "More segmentation settings"): "Mais definições de segmentação",
        ("*", "Show advanced segmentation options"): "Mostrar opções avançadas de segmentação",
        ("*", "More connection settings"): "Mais definições de ligação",
        ("*", "Show advanced connection/geometry options"): "Mostrar opções avançadas de ligação/geometria",
        ("*", "More tolerance settings"): "Mais definições de tolerância",
        ("*", "Show advanced tolerance options"): "Mostrar opções avançadas de tolerância",
        ("*", "More alignment settings"): "Mais definições de alinhamento",
        ("*", "Show advanced alignment options"): "Mostrar opções avançadas de alinhamento",
        ("*", "Segmentation"): "Segmentação",
        ("*", "Less..."): "Menos...",
        ("*", "Adjust"): "Ajustar",
        ("*", "Connections"): "Ligações",
        ("*", "Add connectors"): "Adicionar conectores",
        ("Operator", "Add connectors"): "Adicionar conectores",
        ("*", "Place connectors (click)"): "Colocar conectores (clique)",
        ("Operator", "Place connectors (click)"): "Colocar conectores (clique)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Escolher faces no modo Objeto (A = alvo, B = móvel)",
        ("*", "A: none"): "A: nenhum",
        ("*", "B: none"): "B: nenhum",
        ("*", "Pick Face A"): "Escolher Face A",
        ("Operator", "Pick Face A"): "Escolher Face A",
        ("*", "Pick Face B"): "Escolher Face B",
        ("Operator", "Pick Face B"): "Escolher Face B",
        ("*", "Align Faces"): "Alinhar faces",
        ("Operator", "Align Faces"): "Alinhar faces",
    },
    "nl_NL": {
        ("*", "Adjust split axis"): "Splitsas aanpassen",
        ("Operator", "Adjust split axis"): "Splitsas aanpassen",
        ("*", "Split axis adjusted."): "Splitsas aangepast.",
        ("*", "Adjust split axis cancelled."): "Aanpassen van de splitsas geannuleerd.",
        ("*", "Planar Split"): "Planaire splitsing",
        ("Operator", "Planar Split"): "Planaire splitsing",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Splitsen in veel onderdelen kan bij dichte meshes even duren...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Automatisch afsluiten vond geen geldige lussen.",
        ("*", "Auto-capped seams on {n} part(s)."): "Automatisch afsluiten toegepast op {n} onderdeel/onderdelen.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Minder onderdelen gemaakt dan verwacht ({have} < {want}).",
        ("*", "{n} parts created."): "{n} onderdelen gemaakt.",
        ("*", "Cap seams now"): "Randen nu afsluiten",
        ("Operator", "Cap seams now"): "Randen nu afsluiten",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Vullen tussen precies twee split-randlussen (buiten+binnen) per vlak. Seeds hebben voorkeur.",
        ("*", "Only selected objects"): "Alleen geselecteerde objecten",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = alle vlakken per object, 1 = alleen grootste",
        ("*", "Select only (no fill)"): "Alleen selecteren (niet vullen)",
        ("*", "Require exactly two seed edges"): "Precies twee seed-randen vereisen",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Als in bewerkmodus precies twee randen zijn geselecteerd, alleen die als seeds gebruiken (geen autodetectie).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Geen mesh-objecten om af te sluiten. Selecteer gesplitste delen of gebruik de onderdelenverzameling.",
        ("*", "Processing failed on '{name}': {err}"): "Verwerking mislukt op '{name}': {err}",
        ("*", "Could not determine split edge loops to select."): "Kon de split-randlussen om te selecteren niet bepalen.",
        ("*", "Could not determine and fill split edge loops."): "Kon de split-randlussen niet bepalen en vullen.",
        ("*", "Selected split edge loops on {n} object(s)."): "Split-randlussen geselecteerd op {n} object(en).",
        ("*", "Capped seams on {n} object(s)."): "Randen afgesloten op {n} object(en).",
        ("*", "Please select a mesh object."): "Selecteer een mesh-object.",
        ("*", "Object has unapplied transforms"): "Object heeft niet-toegepaste transformaties",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Overweeg alle transformaties toe te passen (Ctrl+A) voor precieze en voorspelbare resultaten.",
        ("*", "Split Offset (mm)"): "Splits-offset (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Verschuiving van het snijvlak langs de as (positief in de asrichting)",
        ("*", "Split Axis"): "Splitsas",
        ("*", "Split along X"): "Splits langs X",
        ("*", "Split along Y"): "Splits langs Y",
        ("*", "Split along Z"): "Splits langs Z",
        ("*", "Show split preview"): "Splitsvoorbeeld tonen",
        ("*", "Show temporary orange planes at planned cut positions"): "Tijdelijke oranje vlakken tonen op geplande snijposities",
        ("*", "Number of Parts"): "Aantal onderdelen",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Gewenst aantal segmenten (snijvlakken = onderdelen - 1)",
        ("*", "Cap seams during split"): "Randen afsluiten tijdens splitsen",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Sluit randen automatisch na het splitsen. Met holte/binnenschaal: nauwkeurige vulling van buiten-/binnenlussen; zonder holte: eenvoudige vulling. Kan de looptijd verhogen.",
        ("*", "Connector Type"): "Verbindertype",
        ("*", "Cylinder Pin"): "Cilinderpen",
        ("*", "Dowel pin + socket"): "Paspen + bus",
        ("*", "Rectangular Tenon"): "Rechthoekige pen",
        ("*", "Anti-rotation joint"): "Anti-rotatieverbinding",
        ("*", "Dovetail"): "Zwaluwstaart",
        ("*", "Tapered wedge connector"): "Conische wigverbinder",
        ("*", "Snap Pin"): "Klikpen",
        ("*", "Connector with snap spheres"): "Verbinder met klikkogels",
        ("*", "Snap Tenon"): "Klikpen (rechthoek)",
        ("*", "Rectangular tenon with snap spheres"): "Rechthoekige pen met klikkogels",
        ("*", "Snap Dovetail"): "Klik-zwaluwstaart",
        ("*", "Tapered wedge connector with snap spheres"): "Conische wigverbinder met klikkogels",
        ("*", "Custom Connector"): "Aangepaste verbinder",
        ("*", "Use another mesh object from the scene as connector shape"): "Een ander mesh-object uit de scène gebruiken als verbindervorm",
        ("*", "Select connector object"): "Verbinderobject selecteren",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Mesh-object uit deze scène dat als verbindervorm wordt gebruikt. De lokale Z-as ervan wordt behandeld als insteekrichting; het wordt geschaald volgens de Breedte-/Lengte-/Diepte-waarden hieronder.",
        ("*", "Custom Width (mm)"): "Aangepaste breedte (mm)",
        ("*", "Target size along the object's local X axis"): "Doelgrootte langs de lokale X-as van het object",
        ("*", "Custom Length (mm)"): "Aangepaste lengte (mm)",
        ("*", "Target size along the object's local Y axis"): "Doelgrootte langs de lokale Y-as van het object",
        ("*", "Custom Depth (mm)"): "Aangepaste diepte (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Doelgrootte langs de lokale Z-as van het object (insteekdiepte)",
        ("*", "Please select a connector object for Custom Connector."): "Selecteer een verbinderobject voor de Aangepaste verbinder.",
        ("*", "Selected connector object has no usable mesh data."): "Het geselecteerde verbinderobject bevat geen bruikbare meshgegevens.",
        ("*", "Base size"): "Basisformaat",
        ("*", "Dovetail Width (mm)"): "Zwaluwstaartbreedte (mm)",
        ("*", "Dovetail Length (mm)"): "Zwaluwstaartlengte (mm)",
        ("*", "Length along seam plane (local v)"): "Lengte langs het naadvlak (lokale v)",
        ("*", "Dovetail Depth (mm)"): "Zwaluwstaartdiepte (mm)",
        ("*", "Taper (%)"): "Vernauwing (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Percentage waarmee de punt smaller is dan de basis",
        ("*", "Signed Taper (%)"): "Vernauwing met teken (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Vernauwing met teken langs de insteekrichting. Positief verbreedt, negatief vernauwt. Indien niet nul, overschrijft dit de eenvoudige vernauwing.",
        ("*", "Span Axis"): "Spanwijdte-as",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Automatisch rekt langs de breedte-as van de zwaluwstaart en snijdt bij naar de buitenste zijden; X/Y/Z forceert overloop langs die wereldas als deze in het naadvlak ligt; Geen gebruikt de handmatig ingestelde lengte",
        ("*", "None"): "Geen",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Gebruikt de handmatig ingestelde zwaluwstaartlengte; snijdt randen alleen bij als Harde-zijsnede is ingeschakeld",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Rekt automatisch langs de breedte-as van de zwaluwstaart en snijdt bij naar de buitenste zijden",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Forceert overloop langs de wereld-X-as, als deze in het naadvlak ligt",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Forceert overloop langs de wereld-Y-as, als deze in het naadvlak ligt",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Forceert overloop langs de wereld-Z-as, als deze in het naadvlak ligt",
        ("*", "Forces hard-side cut along this axis."): "Forceert een harde-zijsnede langs deze as.",
        ("*", "Hard-side Cut"): "Harde-zijsnede",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Geeft de voorkeur aan een scherpe zijsnede voor de zwaluwstaart-uitsparing/groef",
        ("*", "Margin (%)"): "Marge (%)",
        ("*", "Trim percentage at both ends of seam span"): "Percentage bijsnijden aan beide uiteinden van de naadspanwijdte",
        ("*", "Placement"): "Plaatsing",
        ("*", "Offset along Width (mm)"): "Offset langs de breedte (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Offset binnen het snijvlak langs de breedte-as (u) om het zwaluwstaartpatroon te verschuiven",
        ("*", "Offset along Length (mm)"): "Offset langs de lengte (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Offset binnen het snijvlak langs de lengte-as (v) om het zwaluwstaartpatroon te verschuiven",
        ("*", "Rotation in plane (deg)"): "Rotatie in het vlak (graden)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Rotatie binnen het snijvlak om het zwaluwstaartpatroon te oriënteren",
        ("*", "Span Mode"): "Spanwijdtemodus",
        ("*", "How the dovetail spans along the seam"): "Hoe de zwaluwstaart zich langs de naad uitstrekt",
        ("*", "Auto"): "Automatisch",
        ("*", "Use full edge-to-edge span of the seam"): "Gebruik de volledige rand-tot-rand-spanwijdte van de naad",
        ("*", "Fixed"): "Vast",
        ("*", "Use a fixed repeating spacing"): "Gebruik een vaste, herhaalde tussenafstand",
        ("*", "Centered"): "Gecentreerd",
        ("*", "Center block(s) with margins"): "Centreer blok(ken) met marges",
        ("*", "Live Preview"): "Live voorbeeld",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Toont een live wireframe-voorbeeld van de verbinderplaatsing (Lijn/Raster) voor de huidige selectie. Beperkt tot 200 voorbeeldobjecten omwille van de prestaties.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Het live voorbeeld van verbinders is gestopt bij 200 objecten; overige punten worden niet weergegeven.",
        ("*", "Distribution"): "Verdeling",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Verdeel verbinders langs een lijn of in een raster over het naadvlak",
        ("*", "Line"): "Lijn",
        ("*", "Place connectors along a line in the seam face"): "Plaats verbinders langs een lijn in het naadvlak",
        ("*", "Grid"): "Raster",
        ("*", "Distribute connectors in a grid over the seam face"): "Verdeel verbinders in een raster over het naadvlak",
        ("*", "Connectors per Seam"): "Verbinders per naad",
        ("*", "Rows (GRID)"): "Rijen (RASTER)",
        ("*", "Number of rows for grid distribution"): "Aantal rijen voor rasterverdeling",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Randmarge langs de naad (en loodrecht in RASTER) als percentage van de onderdeellengte (0–40% aanbevolen)",
        ("*", "Spheres per side"): "Kogels per zijde",
        ("*", "Number of snap spheres per side/around"): "Aantal klikkogels per zijde/rondom",
        ("*", "Sphere Diameter (mm)"): "Kogel diameter (mm)",
        ("*", "Diameter of snap spheres"): "Diameter van de klikkogels",
        ("*", "Protrusion (mm)"): "Uitsteek (mm)",
        ("*", "How far spheres protrude from side surface"): "Hoe ver de kogels uit het zijvlak steken",
        ("*", "Pin Diameter (mm)"): "Pendiameter (mm)",
        ("*", "Pin Length (mm)"): "Penlengte (mm)",
        ("*", "Segments"): "Segmenten",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Radiale segmenten van de cilinderpen (visuele gladheid)",
        ("*", "Tenon Width (mm)"): "Penbreedte (mm)",
        ("*", "Tenon Depth (mm)"): "Pendiepte (mm)",
        ("*", "Chamfer (mm)"): "Afschuining (mm)",
        ("*", "Insert Depth (%)"): "Instekdiepte (%)",
        ("*", "Percentage of connector length recessed into part A"): "Percentage van de connectorlengte verzonken in deel A",
        ("*", "Material Profiles"): "Materiaalprofielen",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Selecteer een materiaalprofiel om de tolerantie per zijde automatisch in te vullen",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Aanbevolen tolerantie per zijde: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolerantie per vlak (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Overschrijft het materiaalprofiel (0 = profielwaarde gebruiken)",
        ("*", "More segmentation settings"): "Meer segmentatie-instellingen",
        ("*", "Show advanced segmentation options"): "Geavanceerde segmentatieopties tonen",
        ("*", "More connection settings"): "Meer verbindingsinstellingen",
        ("*", "Show advanced connection/geometry options"): "Geavanceerde verbindings-/geometrieopties tonen",
        ("*", "More tolerance settings"): "Meer toleranties-instellingen",
        ("*", "Show advanced tolerance options"): "Geavanceerde tolerantiesopties tonen",
        ("*", "More alignment settings"): "Meer uitlijningsinstellingen",
        ("*", "Show advanced alignment options"): "Geavanceerde uitlijningsopties tonen",
        ("*", "Segmentation"): "Segmentatie",
        ("*", "Less..."): "Minder...",
        ("*", "Adjust"): "Aanpassen",
        ("*", "Connections"): "Verbindingen",
        ("*", "Add connectors"): "Verbinders toevoegen",
        ("Operator", "Add connectors"): "Verbinders toevoegen",
        ("*", "Place connectors (click)"): "Verbinders plaatsen (klik)",
        ("Operator", "Place connectors (click)"): "Verbinders plaatsen (klik)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Vlakken kiezen in Objectmodus (A = doel, B = bewegend)",
        ("*", "A: none"): "A: geen",
        ("*", "B: none"): "B: geen",
        ("*", "Pick Face A"): "Kies Vlak A",
        ("Operator", "Pick Face A"): "Kies Vlak A",
        ("*", "Pick Face B"): "Kies Vlak B",
        ("Operator", "Pick Face B"): "Kies Vlak B",
        ("*", "Align Faces"): "Vlakken uitlijnen",
        ("Operator", "Align Faces"): "Vlakken uitlijnen",
    },
    "pl_PL": {
        ("*", "Adjust split axis"): "Dostosuj oś cięcia",
        ("Operator", "Adjust split axis"): "Dostosuj oś cięcia",
        ("*", "Split axis adjusted."): "Oś cięcia dostosowana.",
        ("*", "Adjust split axis cancelled."): "Anulowano dostosowanie osi cięcia.",
        ("*", "Planar Split"): "Cięcie planarzne",
        ("Operator", "Planar Split"): "Cięcie planarzne",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Dzielenie na wiele części może zająć trochę czasu przy gęstych siatkach...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Automatyczne zamykanie nie znalazło prawidłowych pętli.",
        ("*", "Auto-capped seams on {n} part(s)."): "Automatycznie zamknięto krawędzie w {n} częściach.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Utworzono mniej części niż oczekiwano ({have} < {want}).",
        ("*", "{n} parts created."): "Utworzono {n} część/części.",
        ("*", "Cap seams now"): "Zamknij krawędzie teraz",
        ("Operator", "Cap seams now"): "Zamknij krawędzie teraz",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Wypełnij między dokładnie dwiema pętlami krawędzi cięcia (zewnętrzną+wewnętrzną) na płaszczyznę. Preferowane seeds.",
        ("*", "Only selected objects"): "Tylko wybrane obiekty",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = wszystkie płaszczyzny na obiekt, 1 = tylko największa",
        ("*", "Select only (no fill)"): "Tylko zaznacz (bez wypełniania)",
        ("*", "Require exactly two seed edges"): "Wymagaj dokładnie dwóch krawędzi seed",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Jeśli w trybie edycji zaznaczono dokładnie dwie krawędzie, użyj ich tylko jako seeds (bez autodetekcji).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Brak obiektów siatki do zamknięcia. Wybierz podzielone części lub użyj kolekcji części.",
        ("*", "Processing failed on '{name}': {err}"): "Przetwarzanie nie powiodło się dla „{name}”: {err}",
        ("*", "Could not determine split edge loops to select."): "Nie można określić pętli krawędzi cięcia do zaznaczenia.",
        ("*", "Could not determine and fill split edge loops."): "Nie można określić i wypełnić pętli krawędzi cięcia.",
        ("*", "Selected split edge loops on {n} object(s)."): "Zaznaczono pętle krawędzi cięcia w {n} obiekcie/obiektach.",
        ("*", "Capped seams on {n} object(s)."): "Zamknięto krawędzie w {n} obiekcie/obiektach.",
        ("*", "Please select a mesh object."): "Wybierz obiekt siatki.",
        ("*", "Object has unapplied transforms"): "Obiekt ma niezastosowane transformacje",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Rozważ zastosowanie wszystkich transformacji (Ctrl+A), aby uzyskać dokładne i przewidywalne wyniki.",
        ("*", "Split Offset (mm)"): "Przesunięcie cięcia (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Przesunięcie płaszczyzny cięcia wzdłuż osi (dodatnie w kierunku osi)",
        ("*", "Split Axis"): "Oś cięcia",
        ("*", "Split along X"): "Tnij wzdłuż X",
        ("*", "Split along Y"): "Tnij wzdłuż Y",
        ("*", "Split along Z"): "Tnij wzdłuż Z",
        ("*", "Show split preview"): "Pokaż podgląd cięcia",
        ("*", "Show temporary orange planes at planned cut positions"): "Pokaż tymczasowe pomarańczowe płaszczyzny w planowanych pozycjach cięcia",
        ("*", "Number of Parts"): "Liczba części",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Liczba pożądanych segmentów (płaszczyzny cięcia = części - 1)",
        ("*", "Cap seams during split"): "Zamykaj krawędzie podczas cięcia",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Automatycznie zamykaj krawędzie po cięciu. Z wnęką/powłoką wewn.: precyzyjne wypełnienie pętli zewn./wewn.; bez wnęki: proste wypełnienie. Może wydłużyć czas działania.",
        ("*", "Connector Type"): "Typ łącznika",
        ("*", "Cylinder Pin"): "Kołek cylindryczny",
        ("*", "Dowel pin + socket"): "Kołek + tuleja",
        ("*", "Rectangular Tenon"): "Czop prostokątny",
        ("*", "Anti-rotation joint"): "Połączenie przeciwobrotowe",
        ("*", "Dovetail"): "Jaskółczy ogon",
        ("*", "Tapered wedge connector"): "Łącznik klinowy stożkowy",
        ("*", "Snap Pin"): "Kołek zatrzaskowy",
        ("*", "Connector with snap spheres"): "Łącznik z kulkami zatrzaskowymi",
        ("*", "Snap Tenon"): "Czop zatrzaskowy",
        ("*", "Rectangular tenon with snap spheres"): "Prostokątny czop z kulkami zatrzaskowymi",
        ("*", "Snap Dovetail"): "Zatrzaskowy jaskółczy ogon",
        ("*", "Tapered wedge connector with snap spheres"): "Łącznik klinowy stożkowy z kulkami zatrzaskowymi",
        ("*", "Custom Connector"): "Łącznik niestandardowy",
        ("*", "Use another mesh object from the scene as connector shape"): "Użyj innego obiektu siatki ze sceny jako kształtu łącznika",
        ("*", "Select connector object"): "Wybierz obiekt łącznika",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Obiekt siatki z tej sceny użyty jako kształt łącznika. Jego lokalna oś Z jest traktowana jako kierunek wkładania; zostanie przeskalowany zgodnie z wartościami Szerokość/Długość/Głębokość poniżej.",
        ("*", "Custom Width (mm)"): "Niestandardowa szerokość (mm)",
        ("*", "Target size along the object's local X axis"): "Docelowy rozmiar wzdłuż lokalnej osi X obiektu",
        ("*", "Custom Length (mm)"): "Niestandardowa długość (mm)",
        ("*", "Target size along the object's local Y axis"): "Docelowy rozmiar wzdłuż lokalnej osi Y obiektu",
        ("*", "Custom Depth (mm)"): "Niestandardowa głębokość (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Docelowy rozmiar wzdłuż lokalnej osi Z obiektu (głębokość wkładania)",
        ("*", "Please select a connector object for Custom Connector."): "Wybierz obiekt łącznika dla Łącznika niestandardowego.",
        ("*", "Selected connector object has no usable mesh data."): "Wybrany obiekt łącznika nie zawiera użytecznych danych siatki.",
        ("*", "Base size"): "Rozmiar podstawy",
        ("*", "Dovetail Width (mm)"): "Szerokość jaskółczego ogona (mm)",
        ("*", "Dovetail Length (mm)"): "Długość jaskółczego ogona (mm)",
        ("*", "Length along seam plane (local v)"): "Długość wzdłuż płaszczyzny złącza (lokalne v)",
        ("*", "Dovetail Depth (mm)"): "Głębokość jaskółczego ogona (mm)",
        ("*", "Taper (%)"): "Zwężenie (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Procent, o jaki czubek jest węższy od podstawy",
        ("*", "Signed Taper (%)"): "Zwężenie ze znakiem (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Zwężenie ze znakiem wzdłuż wkładania. Dodatnie rozszerza, ujemne zwęża. Jeśli różne od zera, zastępuje proste zwężenie.",
        ("*", "Span Axis"): "Oś rozpiętości",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "Automatyczna rozciąga wzdłuż osi szerokości jaskółczego ogona i przycina w kierunku zewnętrznych boków; X/Y/Z wymuszają wystawanie wzdłuż tej osi świata, jeśli leży w płaszczyźnie złącza; Brak używa ręcznie skonfigurowanej długości",
        ("*", "None"): "Brak",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Używa ręcznie skonfigurowanej długości jaskółczego ogona; przycina krawędzie tylko jeśli włączone jest Cięcie twardej strony",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Automatycznie rozciąga wzdłuż osi szerokości jaskółczego ogona i przycina w kierunku zewnętrznych boków",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Wymusza wystawanie wzdłuż osi świata X, jeśli leży w płaszczyźnie złącza",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Wymusza wystawanie wzdłuż osi świata Y, jeśli leży w płaszczyźnie złącza",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Wymusza wystawanie wzdłuż osi świata Z, jeśli leży w płaszczyźnie złącza",
        ("*", "Forces hard-side cut along this axis."): "Wymusza cięcie twardej strony wzdłuż tej osi.",
        ("*", "Hard-side Cut"): "Cięcie twardej strony",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Preferuje ostre cięcie boczne dla wpustu/rowka jaskółczego ogona",
        ("*", "Margin (%)"): "Margines (%)",
        ("*", "Trim percentage at both ends of seam span"): "Procent przycięcia na obu końcach rozpiętości złącza",
        ("*", "Placement"): "Umiejscowienie",
        ("*", "Offset along Width (mm)"): "Przesunięcie wzdłuż szerokości (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Przesunięcie w płaszczyźnie cięcia wzdłuż osi szerokości (u), aby przesunąć wzór jaskółczego ogona",
        ("*", "Offset along Length (mm)"): "Przesunięcie wzdłuż długości (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Przesunięcie w płaszczyźnie cięcia wzdłuż osi długości (v), aby przesunąć wzór jaskółczego ogona",
        ("*", "Rotation in plane (deg)"): "Obrót w płaszczyźnie (stopnie)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Obrót w płaszczyźnie cięcia w celu zorientowania wzoru jaskółczego ogona",
        ("*", "Span Mode"): "Tryb rozpiętości",
        ("*", "How the dovetail spans along the seam"): "Sposób rozciągania jaskółczego ogona wzdłuż złącza",
        ("*", "Auto"): "Automatyczny",
        ("*", "Use full edge-to-edge span of the seam"): "Użyj pełnej rozpiętości złącza od krawędzi do krawędzi",
        ("*", "Fixed"): "Stały",
        ("*", "Use a fixed repeating spacing"): "Użyj stałego, powtarzającego się odstępu",
        ("*", "Centered"): "Wyśrodkowany",
        ("*", "Center block(s) with margins"): "Wyśrodkuj blok(i) z marginesami",
        ("*", "Live Preview"): "Podgląd na żywo",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Pokazuje podgląd rozmieszczenia łączników (Linia/Siatka) w postaci siatki krawędziowej na żywo dla bieżącego zaznaczenia. Ograniczony do 200 obiektów podglądu ze względu na wydajność.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Podgląd łączników na żywo zatrzymał się przy 200 obiektach; pozostałe punkty nie są wyświetlane.",
        ("*", "Distribution"): "Rozmieszczenie",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Rozmieść łączniki wzdłuż linii lub w siatce na powierzchni szwu",
        ("*", "Line"): "Linia",
        ("*", "Place connectors along a line in the seam face"): "Umieść łączniki wzdłuż linii na powierzchni szwu",
        ("*", "Grid"): "Siatka",
        ("*", "Distribute connectors in a grid over the seam face"): "Rozmieść łączniki w siatce na powierzchni szwu",
        ("*", "Connectors per Seam"): "Łączniki na szew",
        ("*", "Rows (GRID)"): "Rzędy (SIATKA)",
        ("*", "Number of rows for grid distribution"): "Liczba rzędów dla rozmieszczenia w siatce",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Margines krawędzi wzdłuż szwu (i prostopadle w SIATCE) jako procent długości części (zalecane 0–40%)",
        ("*", "Spheres per side"): "Kule na stronę",
        ("*", "Number of snap spheres per side/around"): "Liczba kulek zatrzaskowych na stronę/wokół",
        ("*", "Sphere Diameter (mm)"): "Średnica kuli (mm)",
        ("*", "Diameter of snap spheres"): "Średnica kulek zatrzaskowych",
        ("*", "Protrusion (mm)"): "Wystawanie (mm)",
        ("*", "How far spheres protrude from side surface"): "Jak daleko kule wystają z powierzchni bocznej",
        ("*", "Pin Diameter (mm)"): "Średnica kołka (mm)",
        ("*", "Pin Length (mm)"): "Długość kołka (mm)",
        ("*", "Segments"): "Segmenty",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Segmenty promieniowe kołka cylindrycznego (gładkość wizualna)",
        ("*", "Tenon Width (mm)"): "Szerokość czopa (mm)",
        ("*", "Tenon Depth (mm)"): "Głębokość czopa (mm)",
        ("*", "Chamfer (mm)"): "Fazowanie (mm)",
        ("*", "Insert Depth (%)"): "Głębokość osadzenia (%)",
        ("*", "Percentage of connector length recessed into part A"): "Procent długości łącznika zagłębiony w części A",
        ("*", "Material Profiles"): "Profile materiałów",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Wybierz profil materiału, aby automatycznie wypełnić tolerancję na stronę",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Zalecana tolerancja na stronę: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Tolerancja na powierzchnię (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Nadpisuje profil materiału (0 = użyj wartości z profilu)",
        ("*", "More segmentation settings"): "Więcej ustawień segmentacji",
        ("*", "Show advanced segmentation options"): "Pokaż zaawansowane opcje segmentacji",
        ("*", "More connection settings"): "Więcej ustawień połączeń",
        ("*", "Show advanced connection/geometry options"): "Pokaż zaawansowane opcje połączeń/geometrii",
        ("*", "More tolerance settings"): "Więcej ustawień tolerancji",
        ("*", "Show advanced tolerance options"): "Pokaż zaawansowane opcje tolerancji",
        ("*", "More alignment settings"): "Więcej ustawień wyrównania",
        ("*", "Show advanced alignment options"): "Pokaż zaawansowane opcje wyrównania",
        ("*", "Segmentation"): "Segmentacja",
        ("*", "Less..."): "Mniej...",
        ("*", "Adjust"): "Dostosuj",
        ("*", "Connections"): "Połączenia",
        ("*", "Add connectors"): "Dodaj łączniki",
        ("Operator", "Add connectors"): "Dodaj łączniki",
        ("*", "Place connectors (click)"): "Umieść łączniki (klik)",
        ("Operator", "Place connectors (click)"): "Umieść łączniki (klik)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Wybierz powierzchnie w trybie Obiekt (A = cel, B = ruchoma)",
        ("*", "A: none"): "A: brak",
        ("*", "B: none"): "B: brak",
        ("*", "Pick Face A"): "Wybierz Powierzchnię A",
        ("Operator", "Pick Face A"): "Wybierz Powierzchnię A",
        ("*", "Pick Face B"): "Wybierz Powierzchnię B",
        ("Operator", "Pick Face B"): "Wybierz Powierzchnię B",
        ("*", "Align Faces"): "Wyrównaj powierzchnie",
        ("Operator", "Align Faces"): "Wyrównaj powierzchnie",
    },
    "ja_JP": {
        ("*", "Adjust split axis"): "分割軸を調整",
        ("Operator", "Adjust split axis"): "分割軸を調整",
        ("*", "Split axis adjusted."): "分割軸を調整しました。",
        ("*", "Adjust split axis cancelled."): "分割軸の調整をキャンセルしました。",
        ("*", "Planar Split"): "平面分割",
        ("Operator", "Planar Split"): "平面分割",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "多数のパーツに分割すると、高密度メッシュでは時間がかかる場合があります...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "自動キャップで有効なループが見つかりませんでした。",
        ("*", "Auto-capped seams on {n} part(s)."): "自動キャップを {n} 個のパーツで実行しました。",
        ("*", "Fewer parts created than expected ({have} < {want})."): "期待よりパーツ数が少なく作成されました（{have} < {want}）。",
        ("*", "{n} parts created."): "{n} 個のパーツを作成しました。",
        ("*", "Cap seams now"): "エッジを今すぐキャップ",
        ("Operator", "Cap seams now"): "エッジを今すぐキャップ",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "各平面につき、外側＋内側の2つの分割エッジループ間を充填します。シードを優先します。",
        ("*", "Only selected objects"): "選択オブジェクトのみ",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = 各オブジェクトの全平面、1 = 最大の平面のみ",
        ("*", "Select only (no fill)"): "選択のみ（充填なし）",
        ("*", "Require exactly two seed edges"): "シードエッジをちょうど2本要求",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "編集モードでエッジがちょうど2本選択されている場合、それらのみをシードとして使用します（自動検出なし）。",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "キャップするメッシュオブジェクトがありません。分割パーツを選択するか、パーツコレクションを使用してください。",
        ("*", "Processing failed on '{name}': {err}"): "「{name}」の処理に失敗しました: {err}",
        ("*", "Could not determine split edge loops to select."): "選択する分割エッジループを特定できませんでした。",
        ("*", "Could not determine and fill split edge loops."): "分割エッジループを特定して充填できませんでした。",
        ("*", "Selected split edge loops on {n} object(s)."): "{n} 個のオブジェクトで分割エッジループを選択しました。",
        ("*", "Capped seams on {n} object(s)."): "{n} 個のオブジェクトでエッジをキャップしました。",
        ("*", "Please select a mesh object."): "メッシュオブジェクトを選択してください。",
        ("*", "Object has unapplied transforms"): "オブジェクトに未適用の変換があります",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "正確で予測可能な結果のため、すべての変換（Ctrl+A）の適用を検討してください。",
        ("*", "Split Offset (mm)"): "カットオフセット (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "分割軸に沿ったカット平面のオフセット（軸方向に正）",
        ("*", "Split Axis"): "分割軸",
        ("*", "Split along X"): "X に沿って分割",
        ("*", "Split along Y"): "Y に沿って分割",
        ("*", "Split along Z"): "Z に沿って分割",
        ("*", "Show split preview"): "分割プレビューを表示",
        ("*", "Show temporary orange planes at planned cut positions"): "予定された切断位置に一時的なオレンジ色の平面を表示",
        ("*", "Number of Parts"): "パーツ数",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "希望するセグメント数（切断平面 = パーツ - 1）",
        ("*", "Cap seams during split"): "分割中にエッジをキャップ",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "分割後にエッジを自動的に閉じます。空洞/内殻あり: 外側/内側ループを精密に充填。空洞なし: 単純な充填。実行時間が増える場合があります。",
        ("*", "Connector Type"): "コネクタタイプ",
        ("*", "Cylinder Pin"): "シリンダーピン",
        ("*", "Dowel pin + socket"): "ダボピン + ソケット",
        ("*", "Rectangular Tenon"): "矩形ほぞ",
        ("*", "Anti-rotation joint"): "回り止め接合",
        ("*", "Dovetail"): "あり継ぎ",
        ("*", "Tapered wedge connector"): "円錐形のくさび状コネクタ",
        ("*", "Snap Pin"): "スナップピン",
        ("*", "Connector with snap spheres"): "スナップ球付きコネクタ",
        ("*", "Snap Tenon"): "スナップほぞ",
        ("*", "Rectangular tenon with snap spheres"): "スナップ球付きの矩形ほぞ",
        ("*", "Snap Dovetail"): "スナップあり継ぎ",
        ("*", "Tapered wedge connector with snap spheres"): "スナップ球付きの円錐形くさびコネクタ",
        ("*", "Custom Connector"): "カスタムコネクタ",
        ("*", "Use another mesh object from the scene as connector shape"): "シーン内の別のメッシュオブジェクトをコネクタ形状として使用",
        ("*", "Select connector object"): "コネクタオブジェクトを選択",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "このシーンのメッシュオブジェクトをコネクタ形状として使用します。そのローカルZ軸は挿入方向として扱われ、以下の幅/長さ/深さの値に従って拡大縮小されます。",
        ("*", "Custom Width (mm)"): "カスタム幅 (mm)",
        ("*", "Target size along the object's local X axis"): "オブジェクトのローカルX軸に沿った目標サイズ",
        ("*", "Custom Length (mm)"): "カスタム長さ (mm)",
        ("*", "Target size along the object's local Y axis"): "オブジェクトのローカルY軸に沿った目標サイズ",
        ("*", "Custom Depth (mm)"): "カスタム深さ (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "オブジェクトのローカルZ軸に沿った目標サイズ（挿入深さ）",
        ("*", "Please select a connector object for Custom Connector."): "カスタムコネクタ用のコネクタオブジェクトを選択してください。",
        ("*", "Selected connector object has no usable mesh data."): "選択したコネクタオブジェクトには使用可能なメッシュデータが含まれていません。",
        ("*", "Base size"): "基本サイズ",
        ("*", "Dovetail Width (mm)"): "あり継ぎ幅 (mm)",
        ("*", "Dovetail Length (mm)"): "あり継ぎ長さ (mm)",
        ("*", "Length along seam plane (local v)"): "接合面に沿った長さ（ローカルv）",
        ("*", "Dovetail Depth (mm)"): "あり継ぎ深さ (mm)",
        ("*", "Taper (%)"): "テーパー (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "先端が基部よりも狭くなる割合",
        ("*", "Signed Taper (%)"): "符号付きテーパー (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "挿入方向に沿った符号付きテーパー。正で拡張、負で縮小。ゼロでない場合、単純なテーパーを上書きします。",
        ("*", "Span Axis"): "スパン軸",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "自動はあり継ぎの幅軸に沿って伸び、外側に向かって切り取ります。X/Y/Zは、その軸が接合面内にある場合、そのワールド軸に沿った延長を強制します。なしは手動設定した長さを使用します",
        ("*", "None"): "なし",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "手動設定したあり継ぎ長さを使用します。ハードサイドカットが有効な場合のみ端を切り取ります",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "あり継ぎの幅軸に沿って自動的に伸び、外側に向かって切り取ります",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "接合面内にある場合、ワールドX軸に沿った延長を強制します",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "接合面内にある場合、ワールドY軸に沿った延長を強制します",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "接合面内にある場合、ワールドZ軸に沿った延長を強制します",
        ("*", "Forces hard-side cut along this axis."): "この軸に沿ってハードサイドカットを強制します。",
        ("*", "Hard-side Cut"): "ハードサイドカット",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "あり継ぎのソケット/溝に対して鮮明な側面カットを優先します",
        ("*", "Margin (%)"): "マージン (%)",
        ("*", "Trim percentage at both ends of seam span"): "接合部のスパンの両端で切り取る割合",
        ("*", "Placement"): "配置",
        ("*", "Offset along Width (mm)"): "幅方向のオフセット (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "あり継ぎパターンをずらすため、切断平面内で幅軸（u）に沿ったオフセット",
        ("*", "Offset along Length (mm)"): "長さ方向のオフセット (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "あり継ぎパターンをずらすため、切断平面内で長さ軸（v）に沿ったオフセット",
        ("*", "Rotation in plane (deg)"): "面内回転（度）",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "あり継ぎパターンの向きを調整するため、切断平面内での回転",
        ("*", "Span Mode"): "スパンモード",
        ("*", "How the dovetail spans along the seam"): "あり継ぎが接合部に沿ってどのように広がるか",
        ("*", "Auto"): "自動",
        ("*", "Use full edge-to-edge span of the seam"): "接合部の端から端までの全スパンを使用",
        ("*", "Fixed"): "固定",
        ("*", "Use a fixed repeating spacing"): "固定の繰り返し間隔を使用",
        ("*", "Centered"): "中央揃え",
        ("*", "Center block(s) with margins"): "マージン付きでブロックを中央に配置",
        ("*", "Live Preview"): "ライブプレビュー",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "現在の選択に対するコネクタ配置（ライン/グリッド）のライブワイヤーフレームプレビューを表示します。パフォーマンスのため、プレビューオブジェクトは200個までに制限されます。",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "コネクタのライブプレビューは200個のオブジェクトで停止しました。残りのポイントは表示されません。",
        ("*", "Distribution"): "分布",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "継ぎ目面に沿ってラインまたはグリッドでコネクタを配置",
        ("*", "Line"): "ライン",
        ("*", "Place connectors along a line in the seam face"): "継ぎ目面に沿ってライン状にコネクタを配置",
        ("*", "Grid"): "グリッド",
        ("*", "Distribute connectors in a grid over the seam face"): "継ぎ目面にグリッド状にコネクタを配置",
        ("*", "Connectors per Seam"): "継ぎ目あたりのコネクタ数",
        ("*", "Rows (GRID)"): "行（グリッド）",
        ("*", "Number of rows for grid distribution"): "グリッド分布の行数",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "継ぎ目に沿った（グリッドでは垂直方向も）エッジマージン。部品長さに対する割合（推奨 0–40%）",
        ("*", "Spheres per side"): "片側の球数",
        ("*", "Number of snap spheres per side/around"): "片側/周囲のスナップ球の数",
        ("*", "Sphere Diameter (mm)"): "球直径 (mm)",
        ("*", "Diameter of snap spheres"): "スナップ球の直径",
        ("*", "Protrusion (mm)"): "突出量 (mm)",
        ("*", "How far spheres protrude from side surface"): "球が側面からどれだけ突出するか",
        ("*", "Pin Diameter (mm)"): "ピン直径 (mm)",
        ("*", "Pin Length (mm)"): "ピン長 (mm)",
        ("*", "Segments"): "セグメント",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "シリンダーピンの放射セグメント（見た目の滑らかさ）",
        ("*", "Tenon Width (mm)"): "ほぞ幅 (mm)",
        ("*", "Tenon Depth (mm)"): "ほぞ深さ (mm)",
        ("*", "Chamfer (mm)"): "面取り (mm)",
        ("*", "Insert Depth (%)"): "挿入深さ (%)",
        ("*", "Percentage of connector length recessed into part A"): "コネクタ長のうちパートAに埋め込む割合",
        ("*", "Material Profiles"): "材料プロファイル",
        ("*", "Select a material profile to auto-fill tolerance per side"): "側ごとの公差を自動入力するため材料プロファイルを選択",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "推奨公差（片側）: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "面あたり公差 (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "材料プロファイルを上書き（0 = プロファイル値を使用）",
        ("*", "More segmentation settings"): "詳細なセグメント設定",
        ("*", "Show advanced segmentation options"): "高度なセグメントオプションを表示",
        ("*", "More connection settings"): "詳細な接続設定",
        ("*", "Show advanced connection/geometry options"): "高度な接続/ジオメトリ オプションを表示",
        ("*", "More tolerance settings"): "詳細な公差設定",
        ("*", "Show advanced tolerance options"): "高度な公差オプションを表示",
        ("*", "More alignment settings"): "詳細な位置合わせ設定",
        ("*", "Show advanced alignment options"): "高度な位置合わせオプションを表示",
        ("*", "Segmentation"): "セグメンテーション",
        ("*", "Less..."): "少なく...",
        ("*", "Adjust"): "調整",
        ("*", "Connections"): "接続",
        ("*", "Add connectors"): "コネクタを追加",
        ("Operator", "Add connectors"): "コネクタを追加",
        ("*", "Place connectors (click)"): "コネクタを配置（クリック）",
        ("Operator", "Place connectors (click)"): "コネクタを配置（クリック）",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "オブジェクトモードで面を選ぶ（A = ターゲット, B = 移動）",
        ("*", "A: none"): "A: なし",
        ("*", "B: none"): "B: なし",
        ("*", "Pick Face A"): "面Aを選択",
        ("Operator", "Pick Face A"): "面Aを選択",
        ("*", "Pick Face B"): "面Bを選択",
        ("Operator", "Pick Face B"): "面Bを選択",
        ("*", "Align Faces"): "面を整列",
        ("Operator", "Align Faces"): "面を整列",
    },
    "zh_HANS": {
        ("*", "Adjust split axis"): "调整切割轴",
        ("Operator", "Adjust split axis"): "调整切割轴",
        ("*", "Split axis adjusted."): "切割轴已调整。",
        ("*", "Adjust split axis cancelled."): "已取消调整切割轴。",
        ("*", "Planar Split"): "平面切割",
        ("Operator", "Planar Split"): "平面切割",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "在高密度网格上分割为多个部分可能需要一些时间……",
        ("*", "Auto-cap during split did not find valid loops to fill."): "自动封盖未找到有效的循环。",
        ("*", "Auto-capped seams on {n} part(s)."): "已在 {n} 个部件上自动封盖。",
        ("*", "Fewer parts created than expected ({have} < {want})."): "创建的部件少于预期（{have} < {want}）。",
        ("*", "{n} parts created."): "已创建 {n} 个部件。",
        ("*", "Cap seams now"): "立即封盖边界",
        ("Operator", "Cap seams now"): "立即封盖边界",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "每个平面在外环与内环两条切割边循环之间填充。优先使用种子。",
        ("*", "Only selected objects"): "仅所选对象",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = 每个对象的所有平面，1 = 仅最大平面",
        ("*", "Select only (no fill)"): "仅选择（不填充）",
        ("*", "Require exactly two seed edges"): "需要恰好两条种子边",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "如果编辑模式下恰好选择两条边，仅将其作为种子（不自动检测）。",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "没有可封盖的网格对象。请选择切割部件或使用部件集合。",
        ("*", "Processing failed on '{name}': {err}"): "处理“{name}”失败：{err}",
        ("*", "Could not determine split edge loops to select."): "无法确定要选择的切割边循环。",
        ("*", "Could not determine and fill split edge loops."): "无法确定并填充切割边循环。",
        ("*", "Selected split edge loops on {n} object(s)."): "已在 {n} 个对象上选择切割边循环。",
        ("*", "Capped seams on {n} object(s)."): "已在 {n} 个对象上封盖边界。",
        ("*", "Please select a mesh object."): "请选择一个网格对象。",
        ("*", "Object has unapplied transforms"): "对象存在未应用的变换",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "为获得精确且可预测的结果，请考虑应用所有变换（Ctrl+A）。",
        ("*", "Split Offset (mm)"): "切割偏移 (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "沿切割轴方向的切割平面偏移量（轴方向为正）",
        ("*", "Split Axis"): "切割轴",
        ("*", "Split along X"): "沿 X 切割",
        ("*", "Split along Y"): "沿 Y 切割",
        ("*", "Split along Z"): "沿 Z 切割",
        ("*", "Show split preview"): "显示切割预览",
        ("*", "Show temporary orange planes at planned cut positions"): "在计划的切割位置显示临时的橙色平面",
        ("*", "Number of Parts"): "部件数量",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "所需的分段数量（切割平面 = 部件 - 1）",
        ("*", "Cap seams during split"): "切割时封盖边界",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "在切割后自动封盖边界。具有空腔/内壳：精确填充外/内环；无空腔：简单填充。可能会增加运行时间。",
        ("*", "Connector Type"): "连接件类型",
        ("*", "Cylinder Pin"): "圆柱销",
        ("*", "Dowel pin + socket"): "圆柱销 + 套筒",
        ("*", "Rectangular Tenon"): "矩形榫",
        ("*", "Anti-rotation joint"): "防转连接",
        ("*", "Dovetail"): "燕尾",
        ("*", "Tapered wedge connector"): "锥形楔形连接件",
        ("*", "Snap Pin"): "卡扣销",
        ("*", "Connector with snap spheres"): "带卡扣球的连接件",
        ("*", "Snap Tenon"): "卡扣榫",
        ("*", "Rectangular tenon with snap spheres"): "带卡扣球的矩形榫",
        ("*", "Snap Dovetail"): "卡扣燕尾",
        ("*", "Tapered wedge connector with snap spheres"): "带卡扣球的锥形楔形连接件",
        ("*", "Custom Connector"): "自定义连接件",
        ("*", "Use another mesh object from the scene as connector shape"): "使用场景中的其他网格对象作为连接件形状",
        ("*", "Select connector object"): "选择连接件对象",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "使用此场景中的网格对象作为连接件形状。其局部 Z 轴被视为插入方向；将根据下面的宽度/长度/深度值进行缩放。",
        ("*", "Custom Width (mm)"): "自定义宽度 (mm)",
        ("*", "Target size along the object's local X axis"): "沿对象局部 X 轴的目标尺寸",
        ("*", "Custom Length (mm)"): "自定义长度 (mm)",
        ("*", "Target size along the object's local Y axis"): "沿对象局部 Y 轴的目标尺寸",
        ("*", "Custom Depth (mm)"): "自定义深度 (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "沿对象局部 Z 轴的目标尺寸（插入深度）",
        ("*", "Please select a connector object for Custom Connector."): "请为自定义连接件选择一个连接件对象。",
        ("*", "Selected connector object has no usable mesh data."): "所选连接件对象不包含可用的网格数据。",
        ("*", "Base size"): "基础尺寸",
        ("*", "Dovetail Width (mm)"): "燕尾宽度 (mm)",
        ("*", "Dovetail Length (mm)"): "燕尾长度 (mm)",
        ("*", "Length along seam plane (local v)"): "沿接缝平面的长度（局部 v）",
        ("*", "Dovetail Depth (mm)"): "燕尾深度 (mm)",
        ("*", "Taper (%)"): "锥度 (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "尖端比底部窄的百分比",
        ("*", "Signed Taper (%)"): "带符号锥度 (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "沿插入方向的带符号锥度。正值加宽，负值收窄。若不为零，将覆盖简单锥度。",
        ("*", "Span Axis"): "跨度轴",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "“自动”沿燕尾宽度轴延伸并向外侧裁切；X/Y/Z 会在该轴位于接缝平面内时强制沿该世界轴延伸；“无”使用手动设置的长度",
        ("*", "None"): "无",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "使用手动设置的燕尾长度；仅当启用硬边切割时才裁切边缘",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "自动沿燕尾宽度轴延伸并向外侧裁切",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "若位于接缝平面内，则强制沿世界 X 轴延伸",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "若位于接缝平面内，则强制沿世界 Y 轴延伸",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "若位于接缝平面内，则强制沿世界 Z 轴延伸",
        ("*", "Forces hard-side cut along this axis."): "沿此轴强制进行硬边切割。",
        ("*", "Hard-side Cut"): "硬边切割",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "优先为燕尾插槽/凹槽提供锐利的侧边切割",
        ("*", "Margin (%)"): "边距 (%)",
        ("*", "Trim percentage at both ends of seam span"): "接缝跨度两端裁切的百分比",
        ("*", "Placement"): "定位",
        ("*", "Offset along Width (mm)"): "沿宽度方向偏移 (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "在切割平面内沿宽度轴（u）的偏移，用于移动燕尾图案",
        ("*", "Offset along Length (mm)"): "沿长度方向偏移 (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "在切割平面内沿长度轴（v）的偏移，用于移动燕尾图案",
        ("*", "Rotation in plane (deg)"): "平面内旋转（度）",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "在切割平面内旋转，以调整燕尾图案的方向",
        ("*", "Span Mode"): "跨度模式",
        ("*", "How the dovetail spans along the seam"): "燕尾沿接缝延伸的方式",
        ("*", "Auto"): "自动",
        ("*", "Use full edge-to-edge span of the seam"): "使用接缝从边到边的完整跨度",
        ("*", "Fixed"): "固定",
        ("*", "Use a fixed repeating spacing"): "使用固定的重复间距",
        ("*", "Centered"): "居中",
        ("*", "Center block(s) with margins"): "使用边距将块居中",
        ("*", "Live Preview"): "实时预览",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "为当前选择显示连接件放置（直线/网格）的实时线框预览。出于性能考虑，预览对象数量限制为 200 个。",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "连接件实时预览在 200 个对象处停止；其余点不会显示。",
        ("*", "Distribution"): "分布",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "沿线或在网格中分布连接件，覆盖接缝面",
        ("*", "Line"): "直线",
        ("*", "Place connectors along a line in the seam face"): "沿接缝面上的直线放置连接件",
        ("*", "Grid"): "网格",
        ("*", "Distribute connectors in a grid over the seam face"): "在接缝面上以网格形式分布连接件",
        ("*", "Connectors per Seam"): "每个接缝的连接件数量",
        ("*", "Rows (GRID)"): "行数（网格）",
        ("*", "Number of rows for grid distribution"): "网格分布的行数",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "沿接缝（以及网格中垂直方向）的边缘边距，占部件长度的百分比（建议 0–40%）",
        ("*", "Spheres per side"): "每侧球数",
        ("*", "Number of snap spheres per side/around"): "每侧/周围的卡扣球数量",
        ("*", "Sphere Diameter (mm)"): "球直径 (mm)",
        ("*", "Diameter of snap spheres"): "卡扣球的直径",
        ("*", "Protrusion (mm)"): "突出量 (mm)",
        ("*", "How far spheres protrude from side surface"): "球从侧面表面突出的距离",
        ("*", "Pin Diameter (mm)"): "销直径 (mm)",
        ("*", "Pin Length (mm)"): "销长度 (mm)",
        ("*", "Segments"): "分段数",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "圆柱销的径向分段数（视觉平滑度）",
        ("*", "Tenon Width (mm)"): "榫宽 (mm)",
        ("*", "Tenon Depth (mm)"): "榫深 (mm)",
        ("*", "Chamfer (mm)"): "倒角 (mm)",
        ("*", "Insert Depth (%)"): "插入深度 (%)",
        ("*", "Percentage of connector length recessed into part A"): "嵌入到部件 A 的连接件长度百分比",
        ("*", "Material Profiles"): "材料配置文件",
        ("*", "Select a material profile to auto-fill tolerance per side"): "选择材料配置文件以自动填充每侧的公差",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "推荐每侧公差：{val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "每个面的公差 (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "覆盖材料配置文件（0 = 使用配置文件值）",
        ("*", "More segmentation settings"): "更多分割设置",
        ("*", "Show advanced segmentation options"): "显示高级分割选项",
        ("*", "More connection settings"): "更多连接设置",
        ("*", "Show advanced connection/geometry options"): "显示高级连接/几何选项",
        ("*", "More tolerance settings"): "更多公差设置",
        ("*", "Show advanced tolerance options"): "显示高级公差选项",
        ("*", "More alignment settings"): "更多对齐设置",
        ("*", "Show advanced alignment options"): "显示高级对齐选项",
        ("*", "Segmentation"): "分割",
        ("*", "Less..."): "更少...",
        ("*", "Adjust"): "调整",
        ("*", "Connections"): "连接",
        ("*", "Add connectors"): "添加连接件",
        ("Operator", "Add connectors"): "添加连接件",
        ("*", "Place connectors (click)"): "放置连接件（单击）",
        ("Operator", "Place connectors (click)"): "放置连接件（单击）",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "在对象模式中选择面（A = 目标，B = 移动）",
        ("*", "A: none"): "A：无",
        ("*", "B: none"): "B：无",
        ("*", "Pick Face A"): "选择面 A",
        ("Operator", "Pick Face A"): "选择面 A",
        ("*", "Pick Face B"): "选择面 B",
        ("Operator", "Pick Face B"): "选择面 B",
        ("*", "Align Faces"): "对齐面",
        ("Operator", "Align Faces"): "对齐面",
    },
    "zh_HANT": {
        ("*", "Adjust split axis"): "調整切割軸",
        ("Operator", "Adjust split axis"): "調整切割軸",
        ("*", "Split axis adjusted."): "已調整切割軸。",
        ("*", "Adjust split axis cancelled."): "已取消調整切割軸。",
        ("*", "Planar Split"): "平面切割",
        ("Operator", "Planar Split"): "平面切割",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "在高密度網格上分割為多個部分可能需要一些時間……",
        ("*", "Auto-cap during split did not find valid loops to fill."): "自動封蓋未找到有效迴圈。",
        ("*", "Auto-capped seams on {n} part(s)."): "已在 {n} 個部件上自動封蓋。",
        ("*", "Fewer parts created than expected ({have} < {want})."): "建立的部件少於預期（{have} < {want}）。",
        ("*", "{n} parts created."): "已建立 {n} 個部件。",
        ("*", "Cap seams now"): "立即封蓋邊界",
        ("Operator", "Cap seams now"): "立即封蓋邊界",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "每個平面在外圈與內圈兩條切割邊迴圈之間填充。優先使用種子。",
        ("*", "Only selected objects"): "僅選取的物件",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = 每個物件的所有平面，1 = 僅最大平面",
        ("*", "Select only (no fill)"): "僅選取（不填充）",
        ("*", "Require exactly two seed edges"): "需要正好兩條種子邊",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "若在編輯模式中正好選取兩條邊，僅將其作為種子（不自動偵測）。",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "沒有可封蓋的網格物件。請選取切割部件或使用部件集合。",
        ("*", "Processing failed on '{name}': {err}"): "處理「{name}」失敗：{err}",
        ("*", "Could not determine split edge loops to select."): "無法判定要選取的切割邊迴圈。",
        ("*", "Could not determine and fill split edge loops."): "無法判定並填充切割邊迴圈。",
        ("*", "Selected split edge loops on {n} object(s)."): "已在 {n} 個物件上選取切割邊迴圈。",
        ("*", "Capped seams on {n} object(s)."): "已在 {n} 個物件上封蓋邊界。",
        ("*", "Please select a mesh object."): "請選取一個網格物件。",
        ("*", "Object has unapplied transforms"): "物件存在未套用的變換",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "為獲得精確且可預期的結果，請考慮套用所有變換（Ctrl+A）。",
        ("*", "Split Offset (mm)"): "切割偏移 (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "沿切割軸方向的切割平面偏移量（軸方向為正）",
        ("*", "Split Axis"): "切割軸",
        ("*", "Split along X"): "沿 X 切割",
        ("*", "Split along Y"): "沿 Y 切割",
        ("*", "Split along Z"): "沿 Z 切割",
        ("*", "Show split preview"): "顯示切割預覽",
        ("*", "Show temporary orange planes at planned cut positions"): "在計畫的切割位置顯示暫時的橘色平面",
        ("*", "Number of Parts"): "部件數量",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "所需的分段數量（切割平面 = 部件 - 1）",
        ("*", "Cap seams during split"): "切割時封蓋邊界",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "在切割後自動封蓋邊界。具有空腔/內殼：精確填充外/內圈；無空腔：簡單填充。可能會增加執行時間。",
        ("*", "Connector Type"): "連接件類型",
        ("*", "Cylinder Pin"): "圓柱銷",
        ("*", "Dowel pin + socket"): "圓柱銷 + 套筒",
        ("*", "Rectangular Tenon"): "矩形榫",
        ("*", "Anti-rotation joint"): "防轉連接",
        ("*", "Dovetail"): "燕尾",
        ("*", "Tapered wedge connector"): "錐形楔形連接件",
        ("*", "Snap Pin"): "卡扣銷",
        ("*", "Connector with snap spheres"): "帶卡扣球的連接件",
        ("*", "Snap Tenon"): "卡扣榫",
        ("*", "Rectangular tenon with snap spheres"): "帶卡扣球的矩形榫",
        ("*", "Snap Dovetail"): "卡扣燕尾",
        ("*", "Tapered wedge connector with snap spheres"): "帶卡扣球的錐形楔形連接件",
        ("*", "Custom Connector"): "自訂連接件",
        ("*", "Use another mesh object from the scene as connector shape"): "使用場景中的其他網格物件作為連接件形狀",
        ("*", "Select connector object"): "選擇連接件物件",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "使用此場景中的網格物件作為連接件形狀。其本地 Z 軸被視為插入方向；將依照下方的寬度/長度/深度值進行縮放。",
        ("*", "Custom Width (mm)"): "自訂寬度 (mm)",
        ("*", "Target size along the object's local X axis"): "沿物件本地 X 軸的目標尺寸",
        ("*", "Custom Length (mm)"): "自訂長度 (mm)",
        ("*", "Target size along the object's local Y axis"): "沿物件本地 Y 軸的目標尺寸",
        ("*", "Custom Depth (mm)"): "自訂深度 (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "沿物件本地 Z 軸的目標尺寸（插入深度）",
        ("*", "Please select a connector object for Custom Connector."): "請為自訂連接件選擇一個連接件物件。",
        ("*", "Selected connector object has no usable mesh data."): "所選連接件物件不包含可用的網格資料。",
        ("*", "Base size"): "基礎尺寸",
        ("*", "Dovetail Width (mm)"): "燕尾寬度 (mm)",
        ("*", "Dovetail Length (mm)"): "燕尾長度 (mm)",
        ("*", "Length along seam plane (local v)"): "沿接縫平面的長度（本地 v）",
        ("*", "Dovetail Depth (mm)"): "燕尾深度 (mm)",
        ("*", "Taper (%)"): "錐度 (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "尖端比底部窄的百分比",
        ("*", "Signed Taper (%)"): "帶正負號錐度 (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "沿插入方向的帶正負號錐度。正值加寬，負值收窄。若不為零，將覆寫簡單錐度。",
        ("*", "Span Axis"): "跨度軸",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "「自動」沿燕尾寬度軸延伸並向外側裁切；X/Y/Z 會在該軸位於接縫平面內時強制沿該世界軸延伸；「無」使用手動設定的長度",
        ("*", "None"): "無",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "使用手動設定的燕尾長度；僅當啟用硬邊切割時才裁切邊緣",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "自動沿燕尾寬度軸延伸並向外側裁切",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "若位於接縫平面內，則強制沿世界 X 軸延伸",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "若位於接縫平面內，則強制沿世界 Y 軸延伸",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "若位於接縫平面內，則強制沿世界 Z 軸延伸",
        ("*", "Forces hard-side cut along this axis."): "沿此軸強制進行硬邊切割。",
        ("*", "Hard-side Cut"): "硬邊切割",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "優先為燕尾插槽/凹槽提供銳利的側邊切割",
        ("*", "Margin (%)"): "邊距 (%)",
        ("*", "Trim percentage at both ends of seam span"): "接縫跨度兩端裁切的百分比",
        ("*", "Placement"): "定位",
        ("*", "Offset along Width (mm)"): "沿寬度方向偏移 (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "在切割平面內沿寬度軸（u）的偏移，用於移動燕尾圖案",
        ("*", "Offset along Length (mm)"): "沿長度方向偏移 (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "在切割平面內沿長度軸（v）的偏移，用於移動燕尾圖案",
        ("*", "Rotation in plane (deg)"): "平面內旋轉（度）",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "在切割平面內旋轉，以調整燕尾圖案的方向",
        ("*", "Span Mode"): "跨度模式",
        ("*", "How the dovetail spans along the seam"): "燕尾沿接縫延伸的方式",
        ("*", "Auto"): "自動",
        ("*", "Use full edge-to-edge span of the seam"): "使用接縫從邊到邊的完整跨度",
        ("*", "Fixed"): "固定",
        ("*", "Use a fixed repeating spacing"): "使用固定的重複間距",
        ("*", "Centered"): "置中",
        ("*", "Center block(s) with margins"): "使用邊距將區塊置中",
        ("*", "Live Preview"): "即時預覽",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "為目前選取顯示連接件放置（直線/網格）的即時線框預覽。基於效能考量，預覽物件數量限制為 200 個。",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "連接件即時預覽在 200 個物件處停止；其餘的點不會顯示。",
        ("*", "Distribution"): "分佈",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "沿線或在網格中分佈連接件，覆蓋接縫面",
        ("*", "Line"): "直線",
        ("*", "Place connectors along a line in the seam face"): "沿接縫面上的直線放置連接件",
        ("*", "Grid"): "網格",
        ("*", "Distribute connectors in a grid over the seam face"): "在接縫面上以網格形式分佈連接件",
        ("*", "Connectors per Seam"): "每個接縫的連接件數量",
        ("*", "Rows (GRID)"): "行數（網格）",
        ("*", "Number of rows for grid distribution"): "網格分佈的行數",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "沿接縫（以及網格中垂直方向）的邊緣邊距，佔部件長度的百分比（建議 0–40%）",
        ("*", "Spheres per side"): "每側球數",
        ("*", "Number of snap spheres per side/around"): "每側/四周的卡扣球數量",
        ("*", "Sphere Diameter (mm)"): "球直徑 (mm)",
        ("*", "Diameter of snap spheres"): "卡扣球的直徑",
        ("*", "Protrusion (mm)"): "突出量 (mm)",
        ("*", "How far spheres protrude from side surface"): "球從側面表面突出的距離",
        ("*", "Pin Diameter (mm)"): "銷直徑 (mm)",
        ("*", "Pin Length (mm)"): "銷長度 (mm)",
        ("*", "Segments"): "分段數",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "圓柱銷的徑向分段數（視覺平滑度）",
        ("*", "Tenon Width (mm)"): "榫寬 (mm)",
        ("*", "Tenon Depth (mm)"): "榫深 (mm)",
        ("*", "Chamfer (mm)"): "倒角 (mm)",
        ("*", "Insert Depth (%)"): "插入深度 (%)",
        ("*", "Percentage of connector length recessed into part A"): "嵌入到部件 A 的連接件長度百分比",
        ("*", "Material Profiles"): "材料設定檔",
        ("*", "Select a material profile to auto-fill tolerance per side"): "選擇材料設定檔以自動填入每側公差",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "建議每側公差：{val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "每個面的公差 (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "覆寫材料設定檔（0 = 使用設定檔值）",
        ("*", "More segmentation settings"): "更多分割設定",
        ("*", "Show advanced segmentation options"): "顯示進階的分割選項",
        ("*", "More connection settings"): "更多連接設定",
        ("*", "Show advanced connection/geometry options"): "顯示進階的連接/幾何選項",
        ("*", "More tolerance settings"): "更多公差設定",
        ("*", "Show advanced tolerance options"): "顯示進階的公差選項",
        ("*", "More alignment settings"): "更多對齊設定",
        ("*", "Show advanced alignment options"): "顯示進階的對齊選項",
        ("*", "Segmentation"): "分割",
        ("*", "Less..."): "更少...",
        ("*", "Adjust"): "調整",
        ("*", "Connections"): "連接",
        ("*", "Add connectors"): "新增連接件",
        ("Operator", "Add connectors"): "新增連接件",
        ("*", "Place connectors (click)"): "放置連接件（點擊）",
        ("Operator", "Place connectors (click)"): "放置連接件（點擊）",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "在物件模式中選擇面（A = 目標，B = 移動）",
        ("*", "A: none"): "A：無",
        ("*", "B: none"): "B：無",
        ("*", "Pick Face A"): "選擇面 A",
        ("Operator", "Pick Face A"): "選擇面 A",
        ("*", "Pick Face B"): "選擇面 B",
        ("Operator", "Pick Face B"): "選擇面 B",
        ("*", "Align Faces"): "對齊面",
        ("Operator", "Align Faces"): "對齊面",
    },
    "ru_RU": {
        ("*", "Adjust split axis"): "Настроить ось разреза",
        ("Operator", "Adjust split axis"): "Настроить ось разреза",
        ("*", "Split axis adjusted."): "Ось разреза настроена.",
        ("*", "Adjust split axis cancelled."): "Настройка оси разреза отменена.",
        ("*", "Planar Split"): "Плоскостной разрез",
        ("Operator", "Planar Split"): "Плоскостной разрез",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Разделение на множество частей может занять время на плотных сетках...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Автозакрытие не нашло допустимых петель.",
        ("*", "Auto-capped seams on {n} part(s)."): "Автозакрытие кромок выполнено на {n} части(ях).",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Создано меньше частей, чем ожидалось ({have} < {want}).",
        ("*", "{n} parts created."): "Создано частей: {n}.",
        ("*", "Cap seams now"): "Закрыть кромки сейчас",
        ("Operator", "Cap seams now"): "Закрыть кромки сейчас",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Заполнить между ровно двумя петлями разреза (внешняя+внутренняя) на плоскость. Seeds предпочтительны.",
        ("*", "Only selected objects"): "Только выбранные объекты",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = все плоскости на объект, 1 = только наибольшая",
        ("*", "Select only (no fill)"): "Только выделение (без заполнения)",
        ("*", "Require exactly two seed edges"): "Требовать ровно две seed-кромки",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Если в режиме редактирования выбраны ровно две кромки, использовать их только как seeds (без автоопределения).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Нет объектов-сеток для закрытия. Выберите разрезанные части или используйте коллекцию частей.",
        ("*", "Processing failed on '{name}': {err}"): "Сбой обработки «{name}»: {err}",
        ("*", "Could not determine split edge loops to select."): "Не удалось определить петли кромок разреза для выделения.",
        ("*", "Could not determine and fill split edge loops."): "Не удалось определить и заполнить петли кромок разреза.",
        ("*", "Selected split edge loops on {n} object(s)."): "Выбраны петли кромок разреза на {n} объект(ах).",
        ("*", "Capped seams on {n} object(s)."): "Кромки закрыты на {n} объект(ах).",
        ("*", "Please select a mesh object."): "Выберите объект-сетку.",
        ("*", "Object has unapplied transforms"): "У объекта имеются неприменённые трансформации",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Рассмотрите применение всех трансформаций (Ctrl+A) для точных и предсказуемых результатов.",
        ("*", "Split Offset (mm)"): "Смещение разреза (мм)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Смещение плоскости разреза вдоль оси (положительно по оси)",
        ("*", "Split Axis"): "Ось разреза",
        ("*", "Split along X"): "Разделить вдоль X",
        ("*", "Split along Y"): "Разделить вдоль Y",
        ("*", "Split along Z"): "Разделить вдоль Z",
        ("*", "Show split preview"): "Показать предварительный просмотр разреза",
        ("*", "Show temporary orange planes at planned cut positions"): "Показать временные оранжевые плоскости в запланированных местах разреза",
        ("*", "Number of Parts"): "Количество частей",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Желаемое количество сегментов (плоскости разреза = части - 1)",
        ("*", "Cap seams during split"): "Закрывать кромки при разрезе",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Автоматически закрывать кромки после разреза. С полостью/внутренней оболочкой: точное заполнение внешних/внутренних петель; без полости: простое заполнение. Может увеличить время выполнения.",
        ("*", "Connector Type"): "Тип соединителя",
        ("*", "Cylinder Pin"): "Цилиндрический штифт",
        ("*", "Dowel pin + socket"): "Штифт + втулка",
        ("*", "Rectangular Tenon"): "Прямоугольный шип",
        ("*", "Anti-rotation joint"): "Соединение против проворота",
        ("*", "Dovetail"): "Ласточкин хвост",
        ("*", "Tapered wedge connector"): "Конический клиновидный соединитель",
        ("*", "Snap Pin"): "Защёлкивающийся штифт",
        ("*", "Connector with snap spheres"): "Соединитель с защёлкивающимися шариками",
        ("*", "Snap Tenon"): "Защёлкивающийся шип",
        ("*", "Rectangular tenon with snap spheres"): "Прямоугольный шип с шариками-защёлками",
        ("*", "Snap Dovetail"): "Защёлкивающийся ласточкин хвост",
        ("*", "Tapered wedge connector with snap spheres"): "Конический клиновидный соединитель с защёлкивающимися шариками",
        ("*", "Custom Connector"): "Пользовательский соединитель",
        ("*", "Use another mesh object from the scene as connector shape"): "Использовать другой объект-сетку из сцены в качестве формы соединителя",
        ("*", "Select connector object"): "Выбрать объект-соединитель",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Объект-сетка из этой сцены, используемый как форма соединителя. Его локальная ось Z рассматривается как направление вставки; он будет масштабирован в соответствии со значениями Ширина/Длина/Глубина ниже.",
        ("*", "Custom Width (mm)"): "Пользовательская ширина (мм)",
        ("*", "Target size along the object's local X axis"): "Целевой размер вдоль локальной оси X объекта",
        ("*", "Custom Length (mm)"): "Пользовательская длина (мм)",
        ("*", "Target size along the object's local Y axis"): "Целевой размер вдоль локальной оси Y объекта",
        ("*", "Custom Depth (mm)"): "Пользовательская глубина (мм)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Целевой размер вдоль локальной оси Z объекта (глубина вставки)",
        ("*", "Please select a connector object for Custom Connector."): "Выберите объект-соединитель для Пользовательского соединителя.",
        ("*", "Selected connector object has no usable mesh data."): "Выбранный объект-соединитель не содержит пригодных данных сетки.",
        ("*", "Base size"): "Базовый размер",
        ("*", "Dovetail Width (mm)"): "Ширина ласточкина хвоста (мм)",
        ("*", "Dovetail Length (mm)"): "Длина ласточкина хвоста (мм)",
        ("*", "Length along seam plane (local v)"): "Длина вдоль плоскости шва (локальная v)",
        ("*", "Dovetail Depth (mm)"): "Глубина ласточкина хвоста (мм)",
        ("*", "Taper (%)"): "Сужение (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Процент, на который кончик уже основания",
        ("*", "Signed Taper (%)"): "Сужение со знаком (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Сужение со знаком вдоль направления вставки. Положительное — расширяет, отрицательное — сужает. Если не равно нулю, переопределяет простое сужение.",
        ("*", "Span Axis"): "Ось охвата",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "«Авто» растягивает вдоль оси ширины ласточкина хвоста и обрезает к внешним сторонам; X/Y/Z принудительно вытягивают вдоль этой мировой оси, если она лежит в плоскости шва; «Нет» использует вручную заданную длину",
        ("*", "None"): "Нет",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Использует вручную заданную длину ласточкина хвоста; обрезает края только если включена Жёсткая боковая резка",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Автоматически растягивает вдоль оси ширины ласточкина хвоста и обрезает к внешним сторонам",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Принудительно вытягивает вдоль мировой оси X, если она лежит в плоскости шва",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Принудительно вытягивает вдоль мировой оси Y, если она лежит в плоскости шва",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Принудительно вытягивает вдоль мировой оси Z, если она лежит в плоскости шва",
        ("*", "Forces hard-side cut along this axis."): "Принудительно применяет жёсткую боковую резку вдоль этой оси.",
        ("*", "Hard-side Cut"): "Жёсткая боковая резка",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Предпочитает чёткий боковой срез для гнезда/паза ласточкина хвоста",
        ("*", "Margin (%)"): "Отступ (%)",
        ("*", "Trim percentage at both ends of seam span"): "Процент обрезки на обоих концах охвата шва",
        ("*", "Placement"): "Расположение",
        ("*", "Offset along Width (mm)"): "Смещение вдоль ширины (мм)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Смещение внутри плоскости разреза вдоль оси ширины (u) для сдвига узора ласточкина хвоста",
        ("*", "Offset along Length (mm)"): "Смещение вдоль длины (мм)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Смещение внутри плоскости разреза вдоль оси длины (v) для сдвига узора ласточкина хвоста",
        ("*", "Rotation in plane (deg)"): "Поворот в плоскости (градусы)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Поворот внутри плоскости разреза для ориентации узора ласточкина хвоста",
        ("*", "Span Mode"): "Режим охвата",
        ("*", "How the dovetail spans along the seam"): "Как ласточкин хвост растягивается вдоль шва",
        ("*", "Auto"): "Авто",
        ("*", "Use full edge-to-edge span of the seam"): "Использовать полный охват шва от края до края",
        ("*", "Fixed"): "Фиксированный",
        ("*", "Use a fixed repeating spacing"): "Использовать фиксированный повторяющийся интервал",
        ("*", "Centered"): "По центру",
        ("*", "Center block(s) with margins"): "Центрировать блок(и) с отступами",
        ("*", "Live Preview"): "Живой предпросмотр",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Показывает живой каркасный предпросмотр расположения соединителей (Линия/Сетка) для текущего выделения. Ограничено 200 объектами предпросмотра из соображений производительности.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Живой предпросмотр соединителей остановлен на 200 объектах; оставшиеся точки не отображаются.",
        ("*", "Distribution"): "Распределение",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Распределить соединители вдоль линии или сеткой по поверхности шва",
        ("*", "Line"): "Линия",
        ("*", "Place connectors along a line in the seam face"): "Разместить соединители вдоль линии на поверхности шва",
        ("*", "Grid"): "Сетка",
        ("*", "Distribute connectors in a grid over the seam face"): "Распределить соединители сеткой по поверхности шва",
        ("*", "Connectors per Seam"): "Соединителей на шов",
        ("*", "Rows (GRID)"): "Ряды (СЕТКА)",
        ("*", "Number of rows for grid distribution"): "Количество рядов для распределения сеткой",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Крайовой зазор вдоль шва (и перпендикулярно в СЕТКЕ) как процент длины детали (рекомендуется 0–40%)",
        ("*", "Spheres per side"): "Шариков на сторону",
        ("*", "Number of snap spheres per side/around"): "Количество защёлкивающихся шариков на сторону/вокруг",
        ("*", "Sphere Diameter (mm)"): "Диаметр шара (мм)",
        ("*", "Diameter of snap spheres"): "Диаметр защёлкивающихся шариков",
        ("*", "Protrusion (mm)"): "Выступание (мм)",
        ("*", "How far spheres protrude from side surface"): "Насколько шарики выступают из боковой поверхности",
        ("*", "Pin Diameter (mm)"): "Диаметр штифта (мм)",
        ("*", "Pin Length (mm)"): "Длина штифта (мм)",
        ("*", "Segments"): "Сегменты",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Радиальные сегменты цилиндрического штифта (визуальная гладкость)",
        ("*", "Tenon Width (mm)"): "Ширина шипа (мм)",
        ("*", "Tenon Depth (mm)"): "Глубина шипа (мм)",
        ("*", "Chamfer (mm)"): "Фаска (мм)",
        ("*", "Insert Depth (%)"): "Глубина вставки (%)",
        ("*", "Percentage of connector length recessed into part A"): "Процент длины соединителя, утопленный в деталь A",
        ("*", "Material Profiles"): "Профили материалов",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Выберите профиль материала, чтобы автоматически заполнить допуск на сторону",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Рекомендуемый допуск на сторону: {val:.2f} мм",
        ("*", "Tolerance per Face (mm)"): "Допуск на грань (мм)",
        ("*", "Overrides material profile (0 = use profile value)"): "Переопределяет профиль материала (0 = использовать значение профиля)",
        ("*", "More segmentation settings"): "Дополнительные настройки сегментации",
        ("*", "Show advanced segmentation options"): "Показать расширенные параметры сегментации",
        ("*", "More connection settings"): "Дополнительные настройки соединений",
        ("*", "Show advanced connection/geometry options"): "Показать расширенные параметры соединений/геометрии",
        ("*", "More tolerance settings"): "Дополнительные настройки допусков",
        ("*", "Show advanced tolerance options"): "Показать расширенные параметры допусков",
        ("*", "More alignment settings"): "Дополнительные настройки выравнивания",
        ("*", "Show advanced alignment options"): "Показать расширенные параметры выравнивания",
        ("*", "Segmentation"): "Сегментация",
        ("*", "Less..."): "Меньше...",
        ("*", "Adjust"): "Настроить",
        ("*", "Connections"): "Соединения",
        ("*", "Add connectors"): "Добавить соединители",
        ("Operator", "Add connectors"): "Добавить соединители",
        ("*", "Place connectors (click)"): "Разместить соединители (клик)",
        ("Operator", "Place connectors (click)"): "Разместить соединители (клик)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Выберите грани в режиме Объект (A = цель, B = движ.)",
        ("*", "A: none"): "A: нет",
        ("*", "B: none"): "B: нет",
        ("*", "Pick Face A"): "Выбрать грань A",
        ("Operator", "Pick Face A"): "Выбрать грань A",
        ("*", "Pick Face B"): "Выбрать грань B",
        ("Operator", "Pick Face B"): "Выбрать грань B",
        ("*", "Align Faces"): "Выровнять грани",
        ("Operator", "Align Faces"): "Выровнять грани",
    },
    "uk_UA": {
        ("*", "Anti-rotation joint"): "З’єднання від провертання",
        ("*", "Dovetail"): "Ластівчин хвіст",
        ("*", "Tapered wedge connector"): "Конічний клиноподібний з’єднувач",
        ("*", "Snap Pin"): "Фіксаторний штифт",
        ("*", "Connector with snap spheres"): "З’єднувач зі сферами-защіпками",
        ("*", "Snap Tenon"): "Фіксаторний шип",
        ("*", "Rectangular tenon with snap spheres"): "Прямокутний шип зі сферами-защіпками",
        ("*", "Snap Dovetail"): "Фіксаторний ластівчин хвіст",
        ("*", "Tapered wedge connector with snap spheres"): "Конічний клиноподібний з’єднувач зі сферами-защіпками",
        ("*", "Custom Connector"): "Користувацький з’єднувач",
        ("*", "Use another mesh object from the scene as connector shape"): "Використати інший сітчастий об’єкт зі сцени як форму з’єднувача",
        ("*", "Select connector object"): "Вибрати об’єкт-з’єднувач",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Сітчастий об’єкт з цієї сцени, що використовується як форма з’єднувача. Його локальна вісь Z вважається напрямком вставки; він буде масштабований відповідно до значень Ширина/Довжина/Глибина нижче.",
        ("*", "Custom Width (mm)"): "Користувацька ширина (мм)",
        ("*", "Target size along the object's local X axis"): "Цільовий розмір уздовж локальної осі X об’єкта",
        ("*", "Custom Length (mm)"): "Користувацька довжина (мм)",
        ("*", "Target size along the object's local Y axis"): "Цільовий розмір уздовж локальної осі Y об’єкта",
        ("*", "Custom Depth (mm)"): "Користувацька глибина (мм)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Цільовий розмір уздовж локальної осі Z об’єкта (глибина вставки)",
        ("*", "Please select a connector object for Custom Connector."): "Виберіть об’єкт-з’єднувач для Користувацького з’єднувача.",
        ("*", "Selected connector object has no usable mesh data."): "Вибраний об’єкт-з’єднувач не містить придатних даних сітки.",
        ("*", "Base size"): "Базовий розмір",
        ("*", "Dovetail Width (mm)"): "Ширина ластівчиного хвоста (мм)",
        ("*", "Dovetail Length (mm)"): "Довжина ластівчиного хвоста (мм)",
        ("*", "Length along seam plane (local v)"): "Довжина вздовж площини шва (локальна v)",
        ("*", "Dovetail Depth (mm)"): "Глибина ластівчиного хвоста (мм)",
        ("*", "Taper (%)"): "Звуження (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Відсоток, на який кінчик вужчий за основу",
        ("*", "Signed Taper (%)"): "Звуження зі знаком (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Звуження зі знаком уздовж напрямку вставки. Додатне — розширює, від’ємне — звужує. Якщо не дорівнює нулю, перевизначає просте звуження.",
        ("*", "Span Axis"): "Вісь охоплення",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "«Авто» розтягує вздовж осі ширини ластівчиного хвоста та обрізає до зовнішніх сторін; X/Y/Z примусово витягують уздовж цієї світової осі, якщо вона лежить у площині шва; «Немає» використовує вручну задану довжину",
        ("*", "None"): "Немає",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Використовує вручну задану довжину ластівчиного хвоста; обрізає краї лише якщо увімкнено Жорсткий боковий розріз",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Автоматично розтягує вздовж осі ширини ластівчиного хвоста та обрізає до зовнішніх сторін",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Примусово витягує вздовж світової осі X, якщо вона лежить у площині шва",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Примусово витягує вздовж світової осі Y, якщо вона лежить у площині шва",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Примусово витягує вздовж світової осі Z, якщо вона лежить у площині шва",
        ("*", "Forces hard-side cut along this axis."): "Примусово застосовує жорсткий боковий розріз уздовж цієї осі.",
        ("*", "Hard-side Cut"): "Жорсткий боковий розріз",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Надає перевагу чіткому боковому розрізу для гнізда/пазу ластівчиного хвоста",
        ("*", "Margin (%)"): "Поле (%)",
        ("*", "Trim percentage at both ends of seam span"): "Відсоток обрізки на обох кінцях охоплення шва",
        ("*", "Placement"): "Розташування",
        ("*", "Offset along Width (mm)"): "Зсув уздовж ширини (мм)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Зсув у площині розрізу вздовж осі ширини (u) для зміщення візерунка ластівчиного хвоста",
        ("*", "Offset along Length (mm)"): "Зсув уздовж довжини (мм)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Зсув у площині розрізу вздовж осі довжини (v) для зміщення візерунка ластівчиного хвоста",
        ("*", "Rotation in plane (deg)"): "Поворот у площині (градуси)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Поворот у площині розрізу для орієнтації візерунка ластівчиного хвоста",
        ("*", "Span Mode"): "Режим охоплення",
        ("*", "How the dovetail spans along the seam"): "Як ластівчин хвіст розтягується вздовж шва",
        ("*", "Auto"): "Авто",
        ("*", "Use full edge-to-edge span of the seam"): "Використати повне охоплення шва від краю до краю",
        ("*", "Fixed"): "Фіксований",
        ("*", "Use a fixed repeating spacing"): "Використати фіксований інтервал повторення",
        ("*", "Centered"): "По центру",
        ("*", "Center block(s) with margins"): "Центрувати блок(и) з полями",
        ("*", "Live Preview"): "Живий попередній перегляд",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Показує живий каркасний попередній перегляд розташування з’єднувачів (Лінія/Сітка) для поточного вибору. Обмежено 200 об’єктами попереднього перегляду з міркувань продуктивності.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Живий попередній перегляд з’єднувачів зупинено на 200 об’єктах; решта точок не відображається.",
        ("*", "Distribution"): "Розподіл",
    },
    "tr_TR": {
        ("*", "Anti-rotation joint"): "Dönmeye karşı bağlantı",
        ("*", "Dovetail"): "Kırlangıç Kuyruğu",
        ("*", "Tapered wedge connector"): "Konik kama şeklinde bağlayıcı",
        ("*", "Snap Pin"): "Sistem Pim",
        ("*", "Connector with snap spheres"): "Sistem küreli bağlayıcı",
        ("*", "Snap Tenon"): "Sistem Zıvana",
        ("*", "Rectangular tenon with snap spheres"): "Küreli dikdörtgen zıvana",
        ("*", "Snap Dovetail"): "Sistem Kırlangıç Kuyruğu",
        ("*", "Tapered wedge connector with snap spheres"): "Sistem küreli konik kama şeklinde bağlayıcı",
        ("*", "Custom Connector"): "Özel Bağlayıcı",
        ("*", "Use another mesh object from the scene as connector shape"): "Sahnedeki başka bir ağ nesnesini bağlayıcı şekli olarak kullan",
        ("*", "Select connector object"): "Bağlayıcı nesnesini seç",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Bu sahneden, bağlayıcı şekli olarak kullanılan bir ağ nesnesi. Yerel Z ekseni ekleme yönü olarak kabul edilir; aşağıdaki Genişlik/Uzunluk/Derinlik değerlerine göre ölçeklenir.",
        ("*", "Custom Width (mm)"): "Özel genişlik (mm)",
        ("*", "Target size along the object's local X axis"): "Nesnenin yerel X ekseni boyunca hedef boyut",
        ("*", "Custom Length (mm)"): "Özel uzunluk (mm)",
        ("*", "Target size along the object's local Y axis"): "Nesnenin yerel Y ekseni boyunca hedef boyut",
        ("*", "Custom Depth (mm)"): "Özel derinlik (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Nesnenin yerel Z ekseni boyunca hedef boyut (ekleme derinliği)",
        ("*", "Please select a connector object for Custom Connector."): "Özel Bağlayıcı için bir bağlayıcı nesnesi seçin.",
        ("*", "Selected connector object has no usable mesh data."): "Seçilen bağlayıcı nesnesi kullanılabilir ağ verisi içermiyor.",
        ("*", "Base size"): "Temel boyut",
        ("*", "Dovetail Width (mm)"): "Kırlangıç kuyruğu genişliği (mm)",
        ("*", "Dovetail Length (mm)"): "Kırlangıç kuyruğu uzunluğu (mm)",
        ("*", "Length along seam plane (local v)"): "Dikiş düzlemi boyunca uzunluk (yerel v)",
        ("*", "Dovetail Depth (mm)"): "Kırlangıç kuyruğu derinliği (mm)",
        ("*", "Taper (%)"): "Daralma (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Ucun tabana göre ne kadar dar olduğu yüzdesi",
        ("*", "Signed Taper (%)"): "İşaretli daralma (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Ekleme yönü boyunca işaretli daralma. Pozitif genişletir, negatif daraltır. Sıfır değilse, basit daralmayı geçersiz kılar.",
        ("*", "Span Axis"): "Kapsam ekseni",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "'Otomatik' kırlangıç kuyruğunun genişlik ekseni boyunca uzar ve dış kenarlara kırpar; X/Y/Z, dikiş düzleminde yer alıyorsa o dünya ekseni boyunca zorla uzatır; 'Yok' manuel olarak ayarlanan uzunluğu kullanır",
        ("*", "None"): "Yok",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Manuel olarak ayarlanan kırlangıç kuyruğu uzunluğunu kullanır; kenarları yalnızca Sert Yan Kesim etkinse kırpar",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Kırlangıç kuyruğunun genişlik ekseni boyunca otomatik uzar ve dış kenarlara kırpar",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Dikiş düzleminde yer alıyorsa dünya X ekseni boyunca zorla uzatır",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Dikiş düzleminde yer alıyorsa dünya Y ekseni boyunca zorla uzatır",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Dikiş düzleminde yer alıyorsa dünya Z ekseni boyunca zorla uzatır",
        ("*", "Forces hard-side cut along this axis."): "Bu eksen boyunca sert yan kesimi zorlar.",
        ("*", "Hard-side Cut"): "Sert Yan Kesim",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Kırlangıç kuyruğu yuvası/oluğu için keskin bir yan kesimi tercih eder",
        ("*", "Margin (%)"): "Kenar payı (%)",
        ("*", "Trim percentage at both ends of seam span"): "Dikiş kapsamının her iki ucundaki kırpma yüzdesi",
        ("*", "Placement"): "Yerleşim",
        ("*", "Offset along Width (mm)"): "Genişlik boyunca ofset (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Kırlangıç kuyruğu desenini kaydırmak için kesme düzleminde genişlik ekseni (u) boyunca ofset",
        ("*", "Offset along Length (mm)"): "Uzunluk boyunca ofset (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Kırlangıç kuyruğu desenini kaydırmak için kesme düzleminde uzunluk ekseni (v) boyunca ofset",
        ("*", "Rotation in plane (deg)"): "Düzlem içi döndürme (derece)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Kırlangıç kuyruğu desenini yönlendirmek için kesme düzlemi içinde döndürme",
        ("*", "Span Mode"): "Kapsam modu",
        ("*", "How the dovetail spans along the seam"): "Kırlangıç kuyruğunun dikiş boyunca nasıl uzadığı",
        ("*", "Auto"): "Otomatik",
        ("*", "Use full edge-to-edge span of the seam"): "Dikişin uçtan uca tam kapsamını kullan",
        ("*", "Fixed"): "Sabit",
        ("*", "Use a fixed repeating spacing"): "Sabit bir tekrar aralığı kullan",
        ("*", "Centered"): "Ortalanmış",
        ("*", "Center block(s) with margins"): "Blok(lar)ı kenar paylarıyla ortala",
        ("*", "Live Preview"): "Canlı önizleme",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Geçerli seçim için bağlayıcı yerleşiminin (Hat/Izgara) canlı tel çerçeve önizlemesini gösterir. Performans nedeniyle 200 önizleme nesnesiyle sınırlıdır.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Bağlayıcı canlı önizlemesi 200 nesnede durdu; kalan noktalar gösterilmiyor.",
        ("*", "Distribution"): "Dağıtım",
    },
    "sl": {
        ("*", "Adjust split axis"): "Prilagodi os reza",
        ("Operator", "Adjust split axis"): "Prilagodi os reza",
        ("*", "Split axis adjusted."): "Os reza je prilagojena.",
        ("*", "Adjust split axis cancelled."): "Prilagajanje osi reza je preklicano.",
        ("*", "Planar Split"): "Ravninski rez",
        ("Operator", "Planar Split"): "Ravninski rez",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Delitev na veliko delov lahko traja pri gostih mrežah ...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Samodejno pokrivanje ni našlo veljavnih zank.",
        ("*", "Auto-capped seams on {n} part(s)."): "Samodejno pokrivanje robov na {n} delih.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Ustvarjenih je manj delov kot pričakovano ({have} < {want}).",
        ("*", "{n} parts created."): "Ustvarjenih {n} delov.",
        ("*", "Cap seams now"): "Zdaj pokrij robove",
        ("Operator", "Cap seams now"): "Zdaj pokrij robove",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Zapolni med natanko dvema zankama reza (zunanjo in notranjo) na ravnino. Semena imajo prednost.",
        ("*", "Only selected objects"): "Samo izbrani predmeti",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = vse ravnine na predmet, 1 = samo največja",
        ("*", "Select only (no fill)"): "Samo izberi (brez zapolnitve)",
        ("*", "Require exactly two seed edges"): "Zahtevaj natanko dva semenska roba",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Če sta v urejevalnem načinu izbrana natanko dva robova, ju uporabi samo kot semeni (brez samodejnega zaznavanja).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Ni mrežnih predmetov za pokrivanje. Izberite razrezane dele ali uporabite zbirko delov.",
        ("*", "Processing failed on '{name}': {err}"): "Obdelava »{name}« ni uspela: {err}",
        ("*", "Could not determine split edge loops to select."): "Zank robov reza za izbiro ni bilo mogoče določiti.",
        ("*", "Could not determine and fill split edge loops."): "Zank robov reza ni bilo mogoče določiti in zapolniti.",
        ("*", "Selected split edge loops on {n} object(s)."): "Zanke robov reza izbrane na {n} predmetih.",
        ("*", "Capped seams on {n} object(s)."): "Robovi pokriti na {n} predmetih.",
        ("*", "Please select a mesh object."): "Izberite mrežni predmet.",
        ("*", "Object has unapplied transforms"): "Predmet ima neuveljavljene transformacije",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Za natančne in predvidljive rezultate razmislite o uveljavitvi vseh transformacij (Ctrl+A).",
        ("*", "Split Offset (mm)"): "Zamik reza (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Zamik ravnine reza vzdolž osi (pozitivno v smeri osi)",
        ("*", "Split Axis"): "Os reza",
        ("*", "Split along X"): "Razdeli vzdolž X",
        ("*", "Split along Y"): "Razdeli vzdolž Y",
        ("*", "Split along Z"): "Razdeli vzdolž Z",
        ("*", "Show split preview"): "Prikaži predogled reza",
        ("*", "Show temporary orange planes at planned cut positions"): "Prikaži začasne oranžne ravnine na načrtovanih mestih reza",
        ("*", "Number of Parts"): "Število delov",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Želeno število segmentov (ravnine reza = deli - 1)",
        ("*", "Cap seams during split"): "Pokrij robove med rezanjem",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Samodejno pokrije robove po rezu. S votlino/notranjo lupino: natančno zapolnjevanje zunanjih/notranjih zank; brez votline: preprosto zapolnjevanje. Lahko podaljša čas izvajanja.",
        ("*", "Connector Type"): "Vrsta konektorja",
        ("*", "Cylinder Pin"): "Valjast zatič",
        ("*", "Dowel pin + socket"): "Zatič + tulka",
        ("*", "Rectangular Tenon"): "Pravokotni čep",
        ("*", "Anti-rotation joint"): "Povezava proti vrtenju",
        ("*", "Dovetail"): "Lastovičji rep",
        ("*", "Tapered wedge connector"): "Stožčast klinasti konektor",
        ("*", "Snap Pin"): "Zaskočni zatič",
        ("*", "Connector with snap spheres"): "Konektor z zaskočnimi kroglicami",
        ("*", "Snap Tenon"): "Zaskočni čep",
        ("*", "Rectangular tenon with snap spheres"): "Pravokotni čep z zaskočnimi kroglicami",
        ("*", "Snap Dovetail"): "Zaskočni lastovičji rep",
        ("*", "Tapered wedge connector with snap spheres"): "Stožčast klinasti konektor z zaskočnimi kroglicami",
        ("*", "Custom Connector"): "Konektor po meri",
        ("*", "Use another mesh object from the scene as connector shape"): "Uporabi drug mrežni predmet iz prizora kot obliko konektorja",
        ("*", "Select connector object"): "Izberi predmet konektorja",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Mrežni predmet iz tega prizora, uporabljen kot oblika konektorja. Njegova lokalna os Z se obravnava kot smer vstavljanja; velikost bo prilagojena glede na spodnje vrednosti širine/dolžine/globine.",
        ("*", "Custom Width (mm)"): "Širina po meri (mm)",
        ("*", "Target size along the object's local X axis"): "Ciljna velikost vzdolž lokalne osi X predmeta",
        ("*", "Custom Length (mm)"): "Dolžina po meri (mm)",
        ("*", "Target size along the object's local Y axis"): "Ciljna velikost vzdolž lokalne osi Y predmeta",
        ("*", "Custom Depth (mm)"): "Globina po meri (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Ciljna velikost vzdolž lokalne osi Z predmeta (globina vstavljanja)",
        ("*", "Please select a connector object for Custom Connector."): "Izberite predmet konektorja za konektor po meri.",
        ("*", "Selected connector object has no usable mesh data."): "Izbrani predmet konektorja ne vsebuje uporabnih mrežnih podatkov.",
        ("*", "Base size"): "Osnovna velikost",
        ("*", "Dovetail Width (mm)"): "Širina lastovičjega repa (mm)",
        ("*", "Dovetail Length (mm)"): "Dolžina lastovičjega repa (mm)",
        ("*", "Length along seam plane (local v)"): "Dolžina vzdolž ravnine šiva (lokalna v)",
        ("*", "Dovetail Depth (mm)"): "Globina lastovičjega repa (mm)",
        ("*", "Taper (%)"): "Zožitev (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Odstotek, za koliko je konica ožja od osnove",
        ("*", "Signed Taper (%)"): "Predznačena zožitev (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Predznačena zožitev vzdolž smeri vstavljanja. Pozitivno razširi, negativno zoži. Če ni nič, prepiše preprosto zožitev.",
        ("*", "Span Axis"): "Os razpona",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "»Samodejno« se razteza vzdolž osi širine lastovičjega repa in obreže do zunanjih strani; X/Y/Z prisili raztezanje vzdolž te svetovne osi, če leži v ravnini šiva; »Brez« uporabi ročno nastavljeno dolžino",
        ("*", "None"): "Brez",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Uporabi ročno nastavljeno dolžino lastovičjega repa; obreže robove le, če je omogočen Trdi stranski rez",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Samodejno se razteza vzdolž osi širine lastovičjega repa in obreže do zunanjih strani",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Prisili raztezanje vzdolž svetovne osi X, če leži v ravnini šiva",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Prisili raztezanje vzdolž svetovne osi Y, če leži v ravnini šiva",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Prisili raztezanje vzdolž svetovne osi Z, če leži v ravnini šiva",
        ("*", "Forces hard-side cut along this axis."): "Prisili trdi stranski rez vzdolž te osi.",
        ("*", "Hard-side Cut"): "Trdi stranski rez",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Daje prednost ostremu stranskemu rezu za vtičnico/utor lastovičjega repa",
        ("*", "Margin (%)"): "Rob (%)",
        ("*", "Trim percentage at both ends of seam span"): "Odstotek obrezovanja na obeh koncih razpona šiva",
        ("*", "Placement"): "Postavitev",
        ("*", "Offset along Width (mm)"): "Zamik vzdolž širine (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Zamik znotraj ravnine reza vzdolž osi širine (u) za premik vzorca lastovičjega repa",
        ("*", "Offset along Length (mm)"): "Zamik vzdolž dolžine (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Zamik znotraj ravnine reza vzdolž osi dolžine (v) za premik vzorca lastovičjega repa",
        ("*", "Rotation in plane (deg)"): "Vrtenje v ravnini (stopinje)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Vrtenje znotraj ravnine reza za usmeritev vzorca lastovičjega repa",
        ("*", "Span Mode"): "Način razpona",
        ("*", "How the dovetail spans along the seam"): "Kako se lastovičji rep razteza vzdolž šiva",
        ("*", "Auto"): "Samodejno",
        ("*", "Use full edge-to-edge span of the seam"): "Uporabi celoten razpon šiva od roba do roba",
        ("*", "Fixed"): "Fiksno",
        ("*", "Use a fixed repeating spacing"): "Uporabi fiksen razmik ponavljanja",
        ("*", "Centered"): "Sredinsko",
        ("*", "Center block(s) with margins"): "Sredinsko poravnaj blok(e) z robovi",
        ("*", "Live Preview"): "Predogled v živo",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Prikaže žični predogled postavitve konektorjev (Črta/Mreža) v živo za trenutno izbiro. Zaradi zmogljivosti omejeno na 200 predmetov predogleda.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Predogled konektorjev v živo se je ustavil pri 200 predmetih; preostale točke niso prikazane.",
        ("*", "Distribution"): "Porazdelitev",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Porazdeli konektorje vzdolž črte ali v mreži po površini šiva",
        ("*", "Line"): "Črta",
        ("*", "Place connectors along a line in the seam face"): "Postavi konektorje vzdolž črte na površini šiva",
        ("*", "Grid"): "Mreža",
        ("*", "Distribute connectors in a grid over the seam face"): "Porazdeli konektorje v mreži po površini šiva",
        ("*", "Connectors per Seam"): "Konektorjev na šiv",
        ("*", "Rows (GRID)"): "Vrstice (MREŽA)",
        ("*", "Number of rows for grid distribution"): "Število vrstic za porazdelitev v mreži",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Robni razmik vzdolž šiva (in pravokotno v MREŽI) kot odstotek dolžine dela (priporočeno 0–40 %)",
        ("*", "Spheres per side"): "Kroglic na stran",
        ("*", "Number of snap spheres per side/around"): "Število zaskočnih kroglic na stran/okoli",
        ("*", "Sphere Diameter (mm)"): "Premer kroglice (mm)",
        ("*", "Diameter of snap spheres"): "Premer zaskočnih kroglic",
        ("*", "Protrusion (mm)"): "Izbočenje (mm)",
        ("*", "How far spheres protrude from side surface"): "Kolikšno je izbočenje kroglic iz stranske površine",
        ("*", "Pin Diameter (mm)"): "Premer zatiča (mm)",
        ("*", "Pin Length (mm)"): "Dolžina zatiča (mm)",
        ("*", "Segments"): "Segmenti",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Radialni segmenti valjastega zatiča (vizualna gladkost)",
        ("*", "Tenon Width (mm)"): "Širina čepa (mm)",
        ("*", "Tenon Depth (mm)"): "Globina čepa (mm)",
        ("*", "Chamfer (mm)"): "Faza (mm)",
        ("*", "Insert Depth (%)"): "Globina vstavljanja (%)",
        ("*", "Percentage of connector length recessed into part A"): "Odstotek dolžine konektorja, vgrajen v del A",
        ("*", "Material Profiles"): "Materialni profili",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Izberite materialni profil za samodejno izpolnitev tolerance na stran",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Priporočena toleranca na stran: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Toleranca na ploskev (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Prepiše materialni profil (0 = uporabi vrednost profila)",
        ("*", "More segmentation settings"): "Več nastavitev segmentacije",
        ("*", "Show advanced segmentation options"): "Prikaži napredne možnosti segmentacije",
        ("*", "More connection settings"): "Več nastavitev povezav",
        ("*", "Show advanced connection/geometry options"): "Prikaži napredne možnosti povezav/geometrije",
        ("*", "More tolerance settings"): "Več nastavitev toleranc",
        ("*", "Show advanced tolerance options"): "Prikaži napredne možnosti toleranc",
        ("*", "More alignment settings"): "Več nastavitev poravnave",
        ("*", "Show advanced alignment options"): "Prikaži napredne možnosti poravnave",
        ("*", "Segmentation"): "Segmentacija",
        ("*", "Less..."): "Manj...",
        ("*", "Adjust"): "Prilagodi",
        ("*", "Connections"): "Povezave",
        ("*", "Add connectors"): "Dodaj konektorje",
        ("Operator", "Add connectors"): "Dodaj konektorje",
        ("*", "Place connectors (click)"): "Postavi konektorje (klik)",
        ("Operator", "Place connectors (click)"): "Postavi konektorje (klik)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Izberite ploskve v predmetnem načinu (A = cilj, B = premakljivo)",
        ("*", "A: none"): "A: brez",
        ("*", "B: none"): "B: brez",
        ("*", "Pick Face A"): "Izberi ploskev A",
        ("Operator", "Pick Face A"): "Izberi ploskev A",
        ("*", "Pick Face B"): "Izberi ploskev B",
        ("Operator", "Pick Face B"): "Izberi ploskev B",
        ("*", "Align Faces"): "Poravnaj ploskve",
        ("Operator", "Align Faces"): "Poravnaj ploskve",
    },
    "ko_KR": {
        ("*", "Adjust split axis"): "분할 축 조정",
        ("Operator", "Adjust split axis"): "분할 축 조정",
        ("*", "Split axis adjusted."): "분할 축이 조정되었습니다.",
        ("*", "Adjust split axis cancelled."): "분할 축 조정이 취소되었습니다.",
        ("*", "Planar Split"): "평면 분할",
        ("Operator", "Planar Split"): "평면 분할",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "많은 부분으로 분할하면 조밀한 메시에서 시간이 걸릴 수 있습니다...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "자동 캡핑에서 유효한 루프를 찾지 못했습니다.",
        ("*", "Auto-capped seams on {n} part(s)."): "{n}개 파트에서 자동 캡핑을 수행했습니다.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "예상보다 적은 파트가 생성되었습니다 ({have} < {want}).",
        ("*", "{n} parts created."): "{n}개의 파트가 생성되었습니다.",
        ("*", "Cap seams now"): "지금 가장자리 캡핑",
        ("Operator", "Cap seams now"): "지금 가장자리 캡핑",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "평면당 정확히 두 개의 분할 가장자리 루프(외부+내부) 사이를 채웁니다. 시드가 우선됩니다.",
        ("*", "Only selected objects"): "선택된 오브젝트만",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = 오브젝트당 모든 평면, 1 = 가장 큰 평면만",
        ("*", "Select only (no fill)"): "선택만 (채우지 않음)",
        ("*", "Require exactly two seed edges"): "정확히 두 개의 시드 가장자리 필요",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "편집 모드에서 정확히 두 개의 가장자리가 선택된 경우, 이를 시드로만 사용합니다(자동 감지 없음).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "캡핑할 메시 오브젝트가 없습니다. 분할된 파트를 선택하거나 파트 컬렉션을 사용하세요.",
        ("*", "Processing failed on '{name}': {err}"): "'{name}' 처리 실패: {err}",
        ("*", "Could not determine split edge loops to select."): "선택할 분할 가장자리 루프를 결정할 수 없습니다.",
        ("*", "Could not determine and fill split edge loops."): "분할 가장자리 루프를 결정하고 채울 수 없습니다.",
        ("*", "Selected split edge loops on {n} object(s)."): "{n}개 오브젝트에서 분할 가장자리 루프를 선택했습니다.",
        ("*", "Capped seams on {n} object(s)."): "{n}개 오브젝트에서 가장자리를 캡핑했습니다.",
        ("*", "Please select a mesh object."): "메시 오브젝트를 선택하세요.",
        ("*", "Object has unapplied transforms"): "오브젝트에 적용되지 않은 변환이 있습니다",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "정확하고 예측 가능한 결과를 위해 모든 변환(Ctrl+A)을 적용하는 것을 고려하세요.",
        ("*", "Split Offset (mm)"): "절단 오프셋 (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "분할 축을 따른 절단 평면의 오프셋(축 방향으로 양수)",
        ("*", "Split Axis"): "분할 축",
        ("*", "Split along X"): "X축을 따라 분할",
        ("*", "Split along Y"): "Y축을 따라 분할",
        ("*", "Split along Z"): "Z축을 따라 분할",
        ("*", "Show split preview"): "분할 미리보기 표시",
        ("*", "Show temporary orange planes at planned cut positions"): "계획된 절단 위치에 임시 주황색 평면을 표시합니다",
        ("*", "Number of Parts"): "파트 수",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "원하는 세그먼트 수(절단 평면 = 파트 수 - 1)",
        ("*", "Cap seams during split"): "분할 중 가장자리 캡핑",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "분할 후 가장자리를 자동으로 캡핑합니다. 공동/내부 쉘이 있는 경우: 외부/내부 루프를 정밀하게 채움; 공동이 없는 경우: 단순 채움. 실행 시간이 늘어날 수 있습니다.",
        ("*", "Connector Type"): "커넥터 유형",
        ("*", "Cylinder Pin"): "원통형 핀",
        ("*", "Dowel pin + socket"): "핀 + 소켓",
        ("*", "Rectangular Tenon"): "직사각형 촉",
        ("*", "Anti-rotation joint"): "회전 방지 연결",
        ("*", "Dovetail"): "더브테일",
        ("*", "Tapered wedge connector"): "원뿔형 쐐기 커넥터",
        ("*", "Snap Pin"): "스냅 핀",
        ("*", "Connector with snap spheres"): "스냅 볼이 있는 커넥터",
        ("*", "Snap Tenon"): "스냅 촉",
        ("*", "Rectangular tenon with snap spheres"): "스냅 볼이 있는 직사각형 촉",
        ("*", "Snap Dovetail"): "스냅 더브테일",
        ("*", "Tapered wedge connector with snap spheres"): "스냅 볼이 있는 원뿔형 쐐기 커넥터",
        ("*", "Custom Connector"): "사용자 지정 커넥터",
        ("*", "Use another mesh object from the scene as connector shape"): "장면의 다른 메시 오브젝트를 커넥터 형태로 사용합니다",
        ("*", "Select connector object"): "커넥터 오브젝트 선택",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "이 장면의 메시 오브젝트를 커넥터 형태로 사용합니다. 로컬 Z축은 삽입 방향으로 간주되며, 아래의 너비/길이/깊이 값에 따라 스케일이 조정됩니다.",
        ("*", "Custom Width (mm)"): "사용자 지정 너비 (mm)",
        ("*", "Target size along the object's local X axis"): "오브젝트의 로컬 X축을 따른 목표 크기",
        ("*", "Custom Length (mm)"): "사용자 지정 길이 (mm)",
        ("*", "Target size along the object's local Y axis"): "오브젝트의 로컬 Y축을 따른 목표 크기",
        ("*", "Custom Depth (mm)"): "사용자 지정 깊이 (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "오브젝트의 로컬 Z축을 따른 목표 크기(삽입 깊이)",
        ("*", "Please select a connector object for Custom Connector."): "사용자 지정 커넥터에 사용할 커넥터 오브젝트를 선택하세요.",
        ("*", "Selected connector object has no usable mesh data."): "선택한 커넥터 오브젝트에 사용 가능한 메시 데이터가 없습니다.",
        ("*", "Base size"): "기본 크기",
        ("*", "Dovetail Width (mm)"): "더브테일 너비 (mm)",
        ("*", "Dovetail Length (mm)"): "더브테일 길이 (mm)",
        ("*", "Length along seam plane (local v)"): "이음면을 따른 길이(로컬 v)",
        ("*", "Dovetail Depth (mm)"): "더브테일 깊이 (mm)",
        ("*", "Taper (%)"): "테이퍼 (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "끝이 기부보다 좁아지는 비율",
        ("*", "Signed Taper (%)"): "부호 있는 테이퍼 (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "삽입 방향을 따른 부호 있는 테이퍼. 양수는 넓어지고, 음수는 좁아집니다. 0이 아니면 단순 테이퍼를 재정의합니다.",
        ("*", "Span Axis"): "스팬 축",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "'자동'은 더브테일 너비 축을 따라 늘어나며 바깥쪽으로 자릅니다. X/Y/Z는 해당 축이 이음면 안에 있을 경우 그 월드 축을 따라 강제로 확장합니다. '없음'은 수동으로 설정된 길이를 사용합니다",
        ("*", "None"): "없음",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "수동으로 설정된 더브테일 길이를 사용합니다. 하드 사이드 컷이 활성화된 경우에만 가장자리를 자릅니다",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "더브테일 너비 축을 따라 자동으로 늘어나며 바깥쪽으로 자릅니다",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "이음면 안에 있을 경우 월드 X축을 따라 강제로 확장합니다",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "이음면 안에 있을 경우 월드 Y축을 따라 강제로 확장합니다",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "이음면 안에 있을 경우 월드 Z축을 따라 강제로 확장합니다",
        ("*", "Forces hard-side cut along this axis."): "이 축을 따라 하드 사이드 컷을 강제 적용합니다.",
        ("*", "Hard-side Cut"): "하드 사이드 컷",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "더브테일 소켓/홈에 선명한 측면 절단을 우선시합니다",
        ("*", "Margin (%)"): "여백 (%)",
        ("*", "Trim percentage at both ends of seam span"): "이음 스팬 양쪽 끝에서 잘라내는 비율",
        ("*", "Placement"): "배치",
        ("*", "Offset along Width (mm)"): "너비 방향 오프셋 (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "더브테일 패턴을 이동시키기 위해 절단 평면 내에서 너비 축(u)을 따른 오프셋",
        ("*", "Offset along Length (mm)"): "길이 방향 오프셋 (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "더브테일 패턴을 이동시키기 위해 절단 평면 내에서 길이 축(v)을 따른 오프셋",
        ("*", "Rotation in plane (deg)"): "평면 내 회전 (도)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "더브테일 패턴의 방향을 조정하기 위한 절단 평면 내 회전",
        ("*", "Span Mode"): "스팬 모드",
        ("*", "How the dovetail spans along the seam"): "더브테일이 이음을 따라 확장되는 방식",
        ("*", "Auto"): "자동",
        ("*", "Use full edge-to-edge span of the seam"): "이음의 끝에서 끝까지 전체 스팬을 사용합니다",
        ("*", "Fixed"): "고정",
        ("*", "Use a fixed repeating spacing"): "고정된 반복 간격을 사용합니다",
        ("*", "Centered"): "가운데 정렬",
        ("*", "Center block(s) with margins"): "여백을 두고 블록을 가운데 정렬합니다",
        ("*", "Live Preview"): "실시간 미리보기",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "현재 선택 항목에 대한 커넥터 배치(선/그리드)의 실시간 와이어프레임 미리보기를 표시합니다. 성능을 위해 미리보기 오브젝트는 200개로 제한됩니다.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "커넥터 실시간 미리보기가 200개 오브젝트에서 중지되었습니다. 나머지 점은 표시되지 않습니다.",
        ("*", "Distribution"): "분포",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "이음면을 따라 선 또는 그리드로 커넥터를 분포시킵니다",
        ("*", "Line"): "선",
        ("*", "Place connectors along a line in the seam face"): "이음면을 따라 선 형태로 커넥터를 배치합니다",
        ("*", "Grid"): "그리드",
        ("*", "Distribute connectors in a grid over the seam face"): "이음면에 그리드 형태로 커넥터를 분포시킵니다",
        ("*", "Connectors per Seam"): "이음당 커넥터 수",
        ("*", "Rows (GRID)"): "행 (그리드)",
        ("*", "Number of rows for grid distribution"): "그리드 분포의 행 수",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "이음을 따른(그리드에서는 수직 방향도) 가장자리 여백, 파트 길이 대비 백분율(권장 0–40%)",
        ("*", "Spheres per side"): "면당 볼 수",
        ("*", "Number of snap spheres per side/around"): "면당/주변의 스냅 볼 수",
        ("*", "Sphere Diameter (mm)"): "볼 지름 (mm)",
        ("*", "Diameter of snap spheres"): "스냅 볼의 지름",
        ("*", "Protrusion (mm)"): "돌출량 (mm)",
        ("*", "How far spheres protrude from side surface"): "볼이 측면에서 돌출되는 정도",
        ("*", "Pin Diameter (mm)"): "핀 지름 (mm)",
        ("*", "Pin Length (mm)"): "핀 길이 (mm)",
        ("*", "Segments"): "세그먼트",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "원통형 핀의 방사형 세그먼트(시각적 매끄러움)",
        ("*", "Tenon Width (mm)"): "촉 너비 (mm)",
        ("*", "Tenon Depth (mm)"): "촉 깊이 (mm)",
        ("*", "Chamfer (mm)"): "모따기 (mm)",
        ("*", "Insert Depth (%)"): "삽입 깊이 (%)",
        ("*", "Percentage of connector length recessed into part A"): "파트 A에 묻히는 커넥터 길이의 비율",
        ("*", "Material Profiles"): "재질 프로필",
        ("*", "Select a material profile to auto-fill tolerance per side"): "면당 공차를 자동으로 채울 재질 프로필을 선택하세요",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "권장 면당 공차: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "면당 공차 (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "재질 프로필을 재정의합니다(0 = 프로필 값 사용)",
        ("*", "More segmentation settings"): "추가 분할 설정",
        ("*", "Show advanced segmentation options"): "고급 분할 옵션 표시",
        ("*", "More connection settings"): "추가 연결 설정",
        ("*", "Show advanced connection/geometry options"): "고급 연결/기하학 옵션 표시",
        ("*", "More tolerance settings"): "추가 공차 설정",
        ("*", "Show advanced tolerance options"): "고급 공차 옵션 표시",
        ("*", "More alignment settings"): "추가 정렬 설정",
        ("*", "Show advanced alignment options"): "고급 정렬 옵션 표시",
        ("*", "Segmentation"): "분할",
        ("*", "Less..."): "적게...",
        ("*", "Adjust"): "조정",
        ("*", "Connections"): "연결",
        ("*", "Add connectors"): "커넥터 추가",
        ("Operator", "Add connectors"): "커넥터 추가",
        ("*", "Place connectors (click)"): "커넥터 배치 (클릭)",
        ("Operator", "Place connectors (click)"): "커넥터 배치 (클릭)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "오브젝트 모드에서 면을 선택하세요 (A = 대상, B = 이동)",
        ("*", "A: none"): "A: 없음",
        ("*", "B: none"): "B: 없음",
        ("*", "Pick Face A"): "면 A 선택",
        ("Operator", "Pick Face A"): "면 A 선택",
        ("*", "Pick Face B"): "면 B 선택",
        ("Operator", "Pick Face B"): "면 B 선택",
        ("*", "Align Faces"): "면 정렬",
        ("Operator", "Align Faces"): "면 정렬",
    },
    "sw": {
        ("*", "Adjust split axis"): "Rekebisha mhimili wa kukata",
        ("Operator", "Adjust split axis"): "Rekebisha mhimili wa kukata",
        ("*", "Split axis adjusted."): "Mhimili wa kukata umerekebishwa.",
        ("*", "Adjust split axis cancelled."): "Urekebishaji wa mhimili wa kukata umeghairiwa.",
        ("*", "Planar Split"): "Ukataji wa ndege",
        ("Operator", "Planar Split"): "Ukataji wa ndege",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "Kugawanya katika sehemu nyingi kunaweza kuchukua muda kwenye matundu mazito...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "Ufunikaji otomatiki haukupata vitanzi halali.",
        ("*", "Auto-capped seams on {n} part(s)."): "Ufunikaji otomatiki ulifanywa kwenye sehemu {n}.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "Sehemu chache zimeundwa kuliko ilivyotarajiwa ({have} < {want}).",
        ("*", "{n} parts created."): "Sehemu {n} zimeundwa.",
        ("*", "Cap seams now"): "Funika kingo sasa",
        ("Operator", "Cap seams now"): "Funika kingo sasa",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "Jaza kati ya vitanzi viwili haswa vya kingo za kukata (nje+ndani) kwa kila ndege. Mbegu (seeds) hupewa kipaumbele.",
        ("*", "Only selected objects"): "Vitu vilivyochaguliwa pekee",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = ndege zote kwa kila kitu, 1 = kubwa zaidi pekee",
        ("*", "Select only (no fill)"): "Chagua pekee (bila kujaza)",
        ("*", "Require exactly two seed edges"): "Hitaji kingo mbili haswa za mbegu",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "Ikiwa kingo mbili haswa zimechaguliwa katika hali ya kuhariri, zitumike tu kama mbegu (bila utambuzi otomatiki).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "Hakuna vitu vya matundu vya kufunika. Chagua sehemu zilizokatwa au tumia mkusanyiko wa sehemu.",
        ("*", "Processing failed on '{name}': {err}"): "Imeshindwa kuchakata '{name}': {err}",
        ("*", "Could not determine split edge loops to select."): "Imeshindikana kubaini vitanzi vya kingo za kukata vya kuchagua.",
        ("*", "Could not determine and fill split edge loops."): "Imeshindikana kubaini na kujaza vitanzi vya kingo za kukata.",
        ("*", "Selected split edge loops on {n} object(s)."): "Vitanzi vya kingo za kukata vimechaguliwa kwenye vitu {n}.",
        ("*", "Capped seams on {n} object(s)."): "Kingo zimefunikwa kwenye vitu {n}.",
        ("*", "Please select a mesh object."): "Tafadhali chagua kitu cha matundu.",
        ("*", "Object has unapplied transforms"): "Kitu kina mabadiliko ambayo hayajatumika",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "Fikiria kutumia mabadiliko yote (Ctrl+A) kwa matokeo sahihi na yanayotabirika.",
        ("*", "Split Offset (mm)"): "Mkengeuko wa ukataji (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "Mkengeuko wa ndege ya kukata kando ya mhimili wa kugawanya (chanya kwenye mwelekeo wa mhimili)",
        ("*", "Split Axis"): "Mhimili wa kugawanya",
        ("*", "Split along X"): "Gawanya kando ya X",
        ("*", "Split along Y"): "Gawanya kando ya Y",
        ("*", "Split along Z"): "Gawanya kando ya Z",
        ("*", "Show split preview"): "Onyesha muhtasari wa kugawanya",
        ("*", "Show temporary orange planes at planned cut positions"): "Onyesha ndege za rangi ya machungwa za muda katika maeneo yaliyopangwa ya kukata",
        ("*", "Number of Parts"): "Idadi ya sehemu",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "Idadi inayotakiwa ya sehemu (ndege za kukata = sehemu - 1)",
        ("*", "Cap seams during split"): "Funika kingo wakati wa kugawanya",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "Funika kingo kiotomatiki baada ya kugawanya. Ikiwa na tundu/ganda la ndani: ujazaji sahihi wa vitanzi vya nje/ndani; bila tundu: ujazaji rahisi. Inaweza kuongeza muda wa kutekeleza.",
        ("*", "Connector Type"): "Aina ya kiungo",
        ("*", "Cylinder Pin"): "Pini ya silinda",
        ("*", "Dowel pin + socket"): "Pini + soketi",
        ("*", "Rectangular Tenon"): "Tenon ya mstatili",
        ("*", "Anti-rotation joint"): "Kiungo cha kuzuia kuzunguka",
        ("*", "Dovetail"): "Dovetail",
        ("*", "Tapered wedge connector"): "Kiungo cha kabari chenye umbo la koni",
        ("*", "Snap Pin"): "Pini ya kubofya",
        ("*", "Connector with snap spheres"): "Kiungo chenye mipira ya kubofya",
        ("*", "Snap Tenon"): "Tenon ya kubofya",
        ("*", "Rectangular tenon with snap spheres"): "Tenon ya mstatili yenye mipira ya kubofya",
        ("*", "Snap Dovetail"): "Dovetail ya kubofya",
        ("*", "Tapered wedge connector with snap spheres"): "Kiungo cha kabari chenye umbo la koni na mipira ya kubofya",
        ("*", "Custom Connector"): "Kiungo maalum",
        ("*", "Use another mesh object from the scene as connector shape"): "Tumia kitu kingine cha matundu kutoka kwenye eneo la tukio kama umbo la kiungo",
        ("*", "Select connector object"): "Chagua kitu cha kiungo",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "Kitu cha matundu kutoka eneo hili la tukio, kinachotumika kama umbo la kiungo. Mhimili wake wa Z wa ndani unachukuliwa kama mwelekeo wa kuingiza; kitapimwa kulingana na thamani za Upana/Urefu/Kina hapa chini.",
        ("*", "Custom Width (mm)"): "Upana maalum (mm)",
        ("*", "Target size along the object's local X axis"): "Ukubwa unaolengwa kando ya mhimili wa X wa ndani wa kitu",
        ("*", "Custom Length (mm)"): "Urefu maalum (mm)",
        ("*", "Target size along the object's local Y axis"): "Ukubwa unaolengwa kando ya mhimili wa Y wa ndani wa kitu",
        ("*", "Custom Depth (mm)"): "Kina maalum (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "Ukubwa unaolengwa kando ya mhimili wa Z wa ndani wa kitu (kina cha kuingiza)",
        ("*", "Please select a connector object for Custom Connector."): "Chagua kitu cha kiungo kwa Kiungo Maalum.",
        ("*", "Selected connector object has no usable mesh data."): "Kitu cha kiungo kilichochaguliwa hakina data ya matundu inayoweza kutumika.",
        ("*", "Base size"): "Ukubwa wa msingi",
        ("*", "Dovetail Width (mm)"): "Upana wa dovetail (mm)",
        ("*", "Dovetail Length (mm)"): "Urefu wa dovetail (mm)",
        ("*", "Length along seam plane (local v)"): "Urefu kando ya ndege ya mshono (v ya ndani)",
        ("*", "Dovetail Depth (mm)"): "Kina cha dovetail (mm)",
        ("*", "Taper (%)"): "Upunguaji (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "Asilimia ambayo ncha ni nyembamba kuliko msingi",
        ("*", "Signed Taper (%)"): "Upunguaji wenye alama (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "Upunguaji wenye alama kando ya mwelekeo wa kuingiza. Chanya hupanua, hasi hupunguza. Ikiwa si sifuri, hubatilisha upunguaji rahisi.",
        ("*", "Span Axis"): "Mhimili wa upana wa jumla",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "'Otomatiki' hunyoosha kando ya mhimili wa upana wa dovetail na kukata kuelekea pande za nje; X/Y/Z hulazimisha unyoshaji kando ya mhimili huo wa dunia ikiwa upo ndani ya ndege ya mshono; 'Hakuna' hutumia urefu uliowekwa kwa mkono",
        ("*", "None"): "Hakuna",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "Hutumia urefu wa dovetail uliowekwa kwa mkono; hukata kingo tu ikiwa Ukataji Mgumu wa Pembeni umewashwa",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "Hunyoosha kiotomatiki kando ya mhimili wa upana wa dovetail na kukata kuelekea pande za nje",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "Hulazimisha unyoshaji kando ya mhimili wa dunia wa X ikiwa upo ndani ya ndege ya mshono",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "Hulazimisha unyoshaji kando ya mhimili wa dunia wa Y ikiwa upo ndani ya ndege ya mshono",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "Hulazimisha unyoshaji kando ya mhimili wa dunia wa Z ikiwa upo ndani ya ndege ya mshono",
        ("*", "Forces hard-side cut along this axis."): "Hulazimisha ukataji mgumu wa pembeni kando ya mhimili huu.",
        ("*", "Hard-side Cut"): "Ukataji mgumu wa pembeni",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "Hupendelea ukataji mkali wa pembeni kwa soketi/mfereji wa dovetail",
        ("*", "Margin (%)"): "Ukingo (%)",
        ("*", "Trim percentage at both ends of seam span"): "Asilimia ya kukata pande zote mbili za upana wa jumla wa mshono",
        ("*", "Placement"): "Uwekaji",
        ("*", "Offset along Width (mm)"): "Mkengeuko kando ya upana (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "Mkengeuko ndani ya ndege ya kukata kando ya mhimili wa upana (u) kuhamisha muundo wa dovetail",
        ("*", "Offset along Length (mm)"): "Mkengeuko kando ya urefu (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "Mkengeuko ndani ya ndege ya kukata kando ya mhimili wa urefu (v) kuhamisha muundo wa dovetail",
        ("*", "Rotation in plane (deg)"): "Mzunguko ndani ya ndege (digrii)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "Mzunguko ndani ya ndege ya kukata kuelekeza muundo wa dovetail",
        ("*", "Span Mode"): "Hali ya upana wa jumla",
        ("*", "How the dovetail spans along the seam"): "Jinsi dovetail inavyonyoosha kando ya mshono",
        ("*", "Auto"): "Otomatiki",
        ("*", "Use full edge-to-edge span of the seam"): "Tumia upana wote wa mshono kutoka ukingo hadi ukingo",
        ("*", "Fixed"): "Fasta",
        ("*", "Use a fixed repeating spacing"): "Tumia nafasi ya kurudia iliyowekwa",
        ("*", "Centered"): "Katikati",
        ("*", "Center block(s) with margins"): "Weka kizuizi(vizuizi) katikati na kingo",
        ("*", "Live Preview"): "Muhtasari wa moja kwa moja",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "Onyesha muhtasari wa moja kwa moja wa waya wa uwekaji wa viungo (Mstari/Gridi) kwa uchaguzi wa sasa. Umepunguzwa hadi vitu 200 vya muhtasari kwa sababu za utendaji.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "Muhtasari wa moja kwa moja wa viungo umesimama kwenye vitu 200; pointi zilizobaki hazitaonyeshwa.",
        ("*", "Distribution"): "Usambazaji",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "Sambaza viungo kando ya mstari au kwenye gridi juu ya uso wa mshono",
        ("*", "Line"): "Mstari",
        ("*", "Place connectors along a line in the seam face"): "Weka viungo kando ya mstari kwenye uso wa mshono",
        ("*", "Grid"): "Gridi",
        ("*", "Distribute connectors in a grid over the seam face"): "Sambaza viungo kwenye gridi juu ya uso wa mshono",
        ("*", "Connectors per Seam"): "Viungo kwa kila mshono",
        ("*", "Rows (GRID)"): "Safu mlalo (GRIDI)",
        ("*", "Number of rows for grid distribution"): "Idadi ya safu mlalo kwa usambazaji wa gridi",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "Ukingo wa pembeni kando ya mshono (na kwa mpangilio wa wima kwenye GRIDI) kama asilimia ya urefu wa sehemu (inapendekezwa 0-40%)",
        ("*", "Spheres per side"): "Mipira kwa kila upande",
        ("*", "Number of snap spheres per side/around"): "Idadi ya mipira ya kubofya kwa kila upande/kuzunguka",
        ("*", "Sphere Diameter (mm)"): "Kipenyo cha mpira (mm)",
        ("*", "Diameter of snap spheres"): "Kipenyo cha mipira ya kubofya",
        ("*", "Protrusion (mm)"): "Kutokeza (mm)",
        ("*", "How far spheres protrude from side surface"): "Kiasi ambacho mipira inatokeza kutoka kwenye uso wa pembeni",
        ("*", "Pin Diameter (mm)"): "Kipenyo cha pini (mm)",
        ("*", "Pin Length (mm)"): "Urefu wa pini (mm)",
        ("*", "Segments"): "Sehemu",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "Sehemu za radial za pini ya silinda (ulaini wa kuonekana)",
        ("*", "Tenon Width (mm)"): "Upana wa tenon (mm)",
        ("*", "Tenon Depth (mm)"): "Kina cha tenon (mm)",
        ("*", "Chamfer (mm)"): "Ukingo ulionyooshwa (mm)",
        ("*", "Insert Depth (%)"): "Kina cha kuingiza (%)",
        ("*", "Percentage of connector length recessed into part A"): "Asilimia ya urefu wa kiungo kilichojazwa ndani ya sehemu A",
        ("*", "Material Profiles"): "Wasifu wa nyenzo",
        ("*", "Select a material profile to auto-fill tolerance per side"): "Chagua wasifu wa nyenzo kujaza kiotomatiki upungufu unaoruhusiwa kwa kila upande",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "Upungufu unaopendekezwa kwa kila upande: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "Upungufu unaoruhusiwa kwa kila uso (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "Hubatilisha wasifu wa nyenzo (0 = tumia thamani ya wasifu)",
        ("*", "More segmentation settings"): "Mipangilio zaidi ya ugawaji",
        ("*", "Show advanced segmentation options"): "Onyesha chaguo za juu za ugawaji",
        ("*", "More connection settings"): "Mipangilio zaidi ya viunganisho",
        ("*", "Show advanced connection/geometry options"): "Onyesha chaguo za juu za viunganisho/jiometri",
        ("*", "More tolerance settings"): "Mipangilio zaidi ya upungufu unaoruhusiwa",
        ("*", "Show advanced tolerance options"): "Onyesha chaguo za juu za upungufu unaoruhusiwa",
        ("*", "More alignment settings"): "Mipangilio zaidi ya upatanishi",
        ("*", "Show advanced alignment options"): "Onyesha chaguo za juu za upatanishi",
        ("*", "Segmentation"): "Ugawaji",
        ("*", "Less..."): "Kidogo...",
        ("*", "Adjust"): "Rekebisha",
        ("*", "Connections"): "Viunganisho",
        ("*", "Add connectors"): "Ongeza viungo",
        ("Operator", "Add connectors"): "Ongeza viungo",
        ("*", "Place connectors (click)"): "Weka viungo (bofya)",
        ("Operator", "Place connectors (click)"): "Weka viungo (bofya)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "Chagua nyuso katika Hali ya Kitu (A = lengwa, B = inayosogea)",
        ("*", "A: none"): "A: hakuna",
        ("*", "B: none"): "B: hakuna",
        ("*", "Pick Face A"): "Chagua uso A",
        ("Operator", "Pick Face A"): "Chagua uso A",
        ("*", "Pick Face B"): "Chagua uso B",
        ("Operator", "Pick Face B"): "Chagua uso B",
        ("*", "Align Faces"): "Panga nyuso",
        ("Operator", "Align Faces"): "Panga nyuso",
    },
    "ar_EG": {
        ("*", "Adjust split axis"): "ضبط محور القطع",
        ("Operator", "Adjust split axis"): "ضبط محور القطع",
        ("*", "Split axis adjusted."): "تم ضبط محور القطع.",
        ("*", "Adjust split axis cancelled."): "تم إلغاء ضبط محور القطع.",
        ("*", "Planar Split"): "قطع مستوٍ",
        ("Operator", "Planar Split"): "قطع مستوٍ",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "قد يستغرق التقسيم إلى أجزاء كثيرة وقتًا مع الشبكات الكثيفة...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "لم يجد الإغلاق التلقائي أي حلقات صالحة.",
        ("*", "Auto-capped seams on {n} part(s)."): "تم الإغلاق التلقائي على {n} جزء/أجزاء.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "تم إنشاء أجزاء أقل من المتوقع ({have} < {want}).",
        ("*", "{n} parts created."): "تم إنشاء {n} جزء/أجزاء.",
        ("*", "Cap seams now"): "إغلاق الحواف الآن",
        ("Operator", "Cap seams now"): "إغلاق الحواف الآن",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "ملء ما بين حلقتين بالضبط من حواف القطع (خارجية+داخلية) لكل مستوى. تُفضَّل البذور (seeds).",
        ("*", "Only selected objects"): "الكائنات المحددة فقط",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = جميع المستويات لكل كائن، 1 = الأكبر فقط",
        ("*", "Select only (no fill)"): "تحديد فقط (بدون ملء)",
        ("*", "Require exactly two seed edges"): "يتطلب بالضبط حافتَي بذرة",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "إذا تم تحديد حافتين بالضبط في وضع التحرير، استخدمهما كبذور فقط (بدون كشف تلقائي).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "لا توجد كائنات شبكية للإغلاق. حدد الأجزاء المقطوعة أو استخدم مجموعة الأجزاء.",
        ("*", "Processing failed on '{name}': {err}"): "فشلت معالجة '{name}': {err}",
        ("*", "Could not determine split edge loops to select."): "تعذّر تحديد حلقات حواف القطع للاختيار.",
        ("*", "Could not determine and fill split edge loops."): "تعذّر تحديد حلقات حواف القطع وملؤها.",
        ("*", "Selected split edge loops on {n} object(s)."): "تم تحديد حلقات حواف القطع على {n} كائن/كائنات.",
        ("*", "Capped seams on {n} object(s)."): "تم إغلاق الحواف على {n} كائن/كائنات.",
        ("*", "Please select a mesh object."): "الرجاء تحديد كائن شبكي.",
        ("*", "Object has unapplied transforms"): "يحتوي الكائن على تحويلات غير مطبَّقة",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "للحصول على نتائج دقيقة ويمكن التنبؤ بها، فكّر في تطبيق جميع التحويلات (Ctrl+A).",
        ("*", "Split Offset (mm)"): "إزاحة القطع (مم)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "إزاحة مستوى القطع على طول محور التقسيم (موجبة في اتجاه المحور)",
        ("*", "Split Axis"): "محور التقسيم",
        ("*", "Split along X"): "تقسيم على طول X",
        ("*", "Split along Y"): "تقسيم على طول Y",
        ("*", "Split along Z"): "تقسيم على طول Z",
        ("*", "Show split preview"): "إظهار معاينة التقسيم",
        ("*", "Show temporary orange planes at planned cut positions"): "إظهار مستويات برتقالية مؤقتة عند مواضع القطع المخطط لها",
        ("*", "Number of Parts"): "عدد الأجزاء",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "عدد الأجزاء المطلوب (مستويات القطع = الأجزاء - 1)",
        ("*", "Cap seams during split"): "إغلاق الحواف أثناء التقسيم",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "إغلاق الحواف تلقائيًا بعد القطع. مع تجويف/غلاف داخلي: ملء دقيق للحلقات الخارجية/الداخلية؛ بدون تجويف: ملء بسيط. قد يزيد من وقت التنفيذ.",
        ("*", "Connector Type"): "نوع الموصل",
        ("*", "Cylinder Pin"): "دبوس أسطواني",
        ("*", "Dowel pin + socket"): "دبوس + تجويف",
        ("*", "Rectangular Tenon"): "لسان مستطيل",
        ("*", "Anti-rotation joint"): "وصلة مانعة للدوران",
        ("*", "Dovetail"): "ذيل الحمامة",
        ("*", "Tapered wedge connector"): "موصل إسفيني مخروطي",
        ("*", "Snap Pin"): "دبوس تعشيق",
        ("*", "Connector with snap spheres"): "موصل بكرات تعشيق",
        ("*", "Snap Tenon"): "لسان تعشيق",
        ("*", "Rectangular tenon with snap spheres"): "لسان مستطيل بكرات تعشيق",
        ("*", "Snap Dovetail"): "ذيل حمامة بتعشيق",
        ("*", "Tapered wedge connector with snap spheres"): "موصل إسفيني مخروطي بكرات تعشيق",
        ("*", "Custom Connector"): "موصل مخصص",
        ("*", "Use another mesh object from the scene as connector shape"): "استخدام كائن شبكي آخر من المشهد كشكل للموصل",
        ("*", "Select connector object"): "اختيار كائن الموصل",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "كائن شبكي من هذا المشهد يُستخدم كشكل للموصل. يُعتبر محوره Z المحلي اتجاه الإدخال؛ سيتم تحجيمه وفق قيم العرض/الطول/العمق أدناه.",
        ("*", "Custom Width (mm)"): "عرض مخصص (مم)",
        ("*", "Target size along the object's local X axis"): "الحجم المستهدف على طول محور X المحلي للكائن",
        ("*", "Custom Length (mm)"): "طول مخصص (مم)",
        ("*", "Target size along the object's local Y axis"): "الحجم المستهدف على طول محور Y المحلي للكائن",
        ("*", "Custom Depth (mm)"): "عمق مخصص (مم)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "الحجم المستهدف على طول محور Z المحلي للكائن (عمق الإدخال)",
        ("*", "Please select a connector object for Custom Connector."): "الرجاء اختيار كائن موصل للموصل المخصص.",
        ("*", "Selected connector object has no usable mesh data."): "كائن الموصل المحدد لا يحتوي على بيانات شبكية قابلة للاستخدام.",
        ("*", "Base size"): "الحجم الأساسي",
        ("*", "Dovetail Width (mm)"): "عرض ذيل الحمامة (مم)",
        ("*", "Dovetail Length (mm)"): "طول ذيل الحمامة (مم)",
        ("*", "Length along seam plane (local v)"): "الطول على طول مستوى الدرزة (v المحلي)",
        ("*", "Dovetail Depth (mm)"): "عمق ذيل الحمامة (مم)",
        ("*", "Taper (%)"): "نسبة التدقيق (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "النسبة المئوية التي يكون بها الطرف أضيق من القاعدة",
        ("*", "Signed Taper (%)"): "تدقيق موقّع (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "تدقيق موقّع على طول اتجاه الإدخال. القيمة الموجبة توسّع، والسالبة تضيّق. إذا لم تكن صفرًا، تتجاوز التدقيق البسيط.",
        ("*", "Span Axis"): "محور الامتداد",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "\"تلقائي\" يمتد على طول محور عرض ذيل الحمامة ويقصّ إلى الجوانب الخارجية؛ X/Y/Z تفرض الامتداد على طول ذلك المحور العالمي إن كان واقعًا في مستوى الدرزة؛ \"بلا\" يستخدم الطول المحدد يدويًا",
        ("*", "None"): "بلا",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "يستخدم طول ذيل الحمامة المحدد يدويًا؛ يقصّ الحواف فقط إذا تم تفعيل القطع الجانبي الصارم",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "يمتد تلقائيًا على طول محور عرض ذيل الحمامة ويقصّ إلى الجوانب الخارجية",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "يفرض الامتداد على طول المحور العالمي X إن كان واقعًا في مستوى الدرزة",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "يفرض الامتداد على طول المحور العالمي Y إن كان واقعًا في مستوى الدرزة",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "يفرض الامتداد على طول المحور العالمي Z إن كان واقعًا في مستوى الدرزة",
        ("*", "Forces hard-side cut along this axis."): "يفرض قطعًا جانبيًا صارمًا على طول هذا المحور.",
        ("*", "Hard-side Cut"): "قطع جانبي صارم",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "يفضّل قطعًا جانبيًا حادًا لمقبس/أخدود ذيل الحمامة",
        ("*", "Margin (%)"): "الهامش (%)",
        ("*", "Trim percentage at both ends of seam span"): "نسبة القص عند طرفي امتداد الدرزة",
        ("*", "Placement"): "الوضع",
        ("*", "Offset along Width (mm)"): "الإزاحة على طول العرض (مم)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "إزاحة داخل مستوى القطع على طول محور العرض (u) لتحريك نمط ذيل الحمامة",
        ("*", "Offset along Length (mm)"): "الإزاحة على طول الطول (مم)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "إزاحة داخل مستوى القطع على طول محور الطول (v) لتحريك نمط ذيل الحمامة",
        ("*", "Rotation in plane (deg)"): "الدوران داخل المستوى (درجة)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "دوران داخل مستوى القطع لتوجيه نمط ذيل الحمامة",
        ("*", "Span Mode"): "وضع الامتداد",
        ("*", "How the dovetail spans along the seam"): "كيفية امتداد ذيل الحمامة على طول الدرزة",
        ("*", "Auto"): "تلقائي",
        ("*", "Use full edge-to-edge span of the seam"): "استخدام كامل امتداد الدرزة من طرف إلى طرف",
        ("*", "Fixed"): "ثابت",
        ("*", "Use a fixed repeating spacing"): "استخدام تباعد تكراري ثابت",
        ("*", "Centered"): "متمركز",
        ("*", "Center block(s) with margins"): "توسيط الكتلة (الكتل) بهوامش",
        ("*", "Live Preview"): "معاينة حية",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "إظهار معاينة سلكية حية لتوزيع الموصلات (خط/شبكة) للتحديد الحالي. محدودة بـ 200 كائن معاينة لأسباب الأداء.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "توقفت المعاينة الحية للموصلات عند 200 كائن؛ النقاط المتبقية غير معروضة.",
        ("*", "Distribution"): "التوزيع",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "توزيع الموصلات على طول خط أو في شبكة عبر وجه الدرزة",
        ("*", "Line"): "خط",
        ("*", "Place connectors along a line in the seam face"): "وضع الموصلات على طول خط في وجه الدرزة",
        ("*", "Grid"): "شبكة",
        ("*", "Distribute connectors in a grid over the seam face"): "توزيع الموصلات في شبكة عبر وجه الدرزة",
        ("*", "Connectors per Seam"): "الموصلات لكل درزة",
        ("*", "Rows (GRID)"): "الصفوف (شبكة)",
        ("*", "Number of rows for grid distribution"): "عدد الصفوف لتوزيع الشبكة",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "هامش الحافة على طول الدرزة (وعموديًا في الشبكة) كنسبة مئوية من طول الجزء (يُنصح بـ 0-40%)",
        ("*", "Spheres per side"): "الكرات لكل جانب",
        ("*", "Number of snap spheres per side/around"): "عدد كرات التعشيق لكل جانب/حول",
        ("*", "Sphere Diameter (mm)"): "قطر الكرة (مم)",
        ("*", "Diameter of snap spheres"): "قطر كرات التعشيق",
        ("*", "Protrusion (mm)"): "البروز (مم)",
        ("*", "How far spheres protrude from side surface"): "مدى بروز الكرات من السطح الجانبي",
        ("*", "Pin Diameter (mm)"): "قطر الدبوس (مم)",
        ("*", "Pin Length (mm)"): "طول الدبوس (مم)",
        ("*", "Segments"): "المقاطع",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "المقاطع الشعاعية للدبوس الأسطواني (نعومة بصرية)",
        ("*", "Tenon Width (mm)"): "عرض اللسان (مم)",
        ("*", "Tenon Depth (mm)"): "عمق اللسان (مم)",
        ("*", "Chamfer (mm)"): "الشطف (مم)",
        ("*", "Insert Depth (%)"): "عمق الإدخال (%)",
        ("*", "Percentage of connector length recessed into part A"): "النسبة المئوية لطول الموصل المدمج في الجزء أ",
        ("*", "Material Profiles"): "ملفات المواد",
        ("*", "Select a material profile to auto-fill tolerance per side"): "اختر ملف مادة لملء التفاوت لكل جانب تلقائيًا",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "التفاوت الموصى به لكل جانب: {val:.2f} مم",
        ("*", "Tolerance per Face (mm)"): "التفاوت لكل وجه (مم)",
        ("*", "Overrides material profile (0 = use profile value)"): "يتجاوز ملف المادة (0 = استخدام قيمة الملف)",
        ("*", "More segmentation settings"): "المزيد من إعدادات التقسيم",
        ("*", "Show advanced segmentation options"): "إظهار خيارات التقسيم المتقدمة",
        ("*", "More connection settings"): "المزيد من إعدادات الاتصال",
        ("*", "Show advanced connection/geometry options"): "إظهار خيارات الاتصال/الهندسة المتقدمة",
        ("*", "More tolerance settings"): "المزيد من إعدادات التفاوت",
        ("*", "Show advanced tolerance options"): "إظهار خيارات التفاوت المتقدمة",
        ("*", "More alignment settings"): "المزيد من إعدادات المحاذاة",
        ("*", "Show advanced alignment options"): "إظهار خيارات المحاذاة المتقدمة",
        ("*", "Segmentation"): "التقسيم",
        ("*", "Less..."): "أقل...",
        ("*", "Adjust"): "ضبط",
        ("*", "Connections"): "الاتصالات",
        ("*", "Add connectors"): "إضافة موصلات",
        ("Operator", "Add connectors"): "إضافة موصلات",
        ("*", "Place connectors (click)"): "وضع الموصلات (نقر)",
        ("Operator", "Place connectors (click)"): "وضع الموصلات (نقر)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "اختر الأوجه في وضع الكائن (أ = الهدف، ب = المتحرك)",
        ("*", "A: none"): "أ: لا شيء",
        ("*", "B: none"): "ب: لا شيء",
        ("*", "Pick Face A"): "اختيار الوجه أ",
        ("Operator", "Pick Face A"): "اختيار الوجه أ",
        ("*", "Pick Face B"): "اختيار الوجه ب",
        ("Operator", "Pick Face B"): "اختيار الوجه ب",
        ("*", "Align Faces"): "محاذاة الأوجه",
        ("Operator", "Align Faces"): "محاذاة الأوجه",
    },
    "fa_IR": {
        ("*", "Adjust split axis"): "تنظیم محور برش",
        ("Operator", "Adjust split axis"): "تنظیم محور برش",
        ("*", "Split axis adjusted."): "محور برش تنظیم شد.",
        ("*", "Adjust split axis cancelled."): "تنظیم محور برش لغو شد.",
        ("*", "Planar Split"): "برش صفحه‌ای",
        ("Operator", "Planar Split"): "برش صفحه‌ای",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "تقسیم به قطعات زیاد ممکن است روی مش‌های چگال زمان‌بر باشد...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "پوشش خودکار هیچ حلقه معتبری پیدا نکرد.",
        ("*", "Auto-capped seams on {n} part(s)."): "پوشش خودکار روی {n} قطعه انجام شد.",
        ("*", "Fewer parts created than expected ({have} < {want})."): "تعداد قطعات ایجادشده کمتر از حد انتظار است ({have} < {want}).",
        ("*", "{n} parts created."): "{n} قطعه ایجاد شد.",
        ("*", "Cap seams now"): "پوشاندن لبه‌ها اکنون",
        ("Operator", "Cap seams now"): "پوشاندن لبه‌ها اکنون",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "پر کردن بین دقیقاً دو حلقه لبه برش (بیرونی+درونی) در هر صفحه. بذرها (seeds) اولویت دارند.",
        ("*", "Only selected objects"): "فقط اشیاء انتخاب‌شده",
        ("*", "0 = all planes per object, 1 = only largest"): "۰ = همه صفحات هر شیء، ۱ = فقط بزرگ‌ترین",
        ("*", "Select only (no fill)"): "فقط انتخاب (بدون پر کردن)",
        ("*", "Require exactly two seed edges"): "نیازمند دقیقاً دو لبه بذر",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "اگر دقیقاً دو لبه در حالت ویرایش انتخاب شده باشند، فقط از آن‌ها به‌عنوان بذر استفاده کن (بدون تشخیص خودکار).",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "هیچ شیء مشی برای پوشاندن وجود ندارد. قطعات برش‌خورده را انتخاب کنید یا از مجموعه قطعات استفاده کنید.",
        ("*", "Processing failed on '{name}': {err}"): "پردازش '{name}' ناموفق بود: {err}",
        ("*", "Could not determine split edge loops to select."): "تعیین حلقه‌های لبه برش برای انتخاب ممکن نشد.",
        ("*", "Could not determine and fill split edge loops."): "تعیین و پر کردن حلقه‌های لبه برش ممکن نشد.",
        ("*", "Selected split edge loops on {n} object(s)."): "حلقه‌های لبه برش روی {n} شیء انتخاب شدند.",
        ("*", "Capped seams on {n} object(s)."): "لبه‌ها روی {n} شیء پوشانده شدند.",
        ("*", "Please select a mesh object."): "لطفاً یک شیء مشی انتخاب کنید.",
        ("*", "Object has unapplied transforms"): "شیء دارای تبدیل‌های اعمال‌نشده است",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "برای نتایج دقیق و قابل پیش‌بینی، اعمال همه تبدیل‌ها (Ctrl+A) را در نظر بگیرید.",
        ("*", "Split Offset (mm)"): "افست برش (mm)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "افست صفحه برش در امتداد محور تقسیم (مثبت در جهت محور)",
        ("*", "Split Axis"): "محور تقسیم",
        ("*", "Split along X"): "تقسیم در امتداد X",
        ("*", "Split along Y"): "تقسیم در امتداد Y",
        ("*", "Split along Z"): "تقسیم در امتداد Z",
        ("*", "Show split preview"): "نمایش پیش‌نمایش تقسیم",
        ("*", "Show temporary orange planes at planned cut positions"): "نمایش صفحات نارنجی موقت در موقعیت‌های برش برنامه‌ریزی‌شده",
        ("*", "Number of Parts"): "تعداد قطعات",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "تعداد قطعات مطلوب (صفحات برش = قطعات - ۱)",
        ("*", "Cap seams during split"): "پوشاندن درزها حین تقسیم",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "پوشاندن خودکار درزها پس از برش. با حفره/پوسته داخلی: پر کردن دقیق حلقه‌های بیرونی/درونی؛ بدون حفره: پر کردن ساده. ممکن است زمان اجرا را افزایش دهد.",
        ("*", "Connector Type"): "نوع رابط",
        ("*", "Cylinder Pin"): "پین استوانه‌ای",
        ("*", "Dowel pin + socket"): "پین + سوکت",
        ("*", "Rectangular Tenon"): "زبانه مستطیلی",
        ("*", "Anti-rotation joint"): "اتصال ضدچرخش",
        ("*", "Dovetail"): "دم‌چلچله‌ای",
        ("*", "Tapered wedge connector"): "رابط گوه‌ای مخروطی",
        ("*", "Snap Pin"): "پین کلیکی",
        ("*", "Connector with snap spheres"): "رابط با گوی‌های کلیکی",
        ("*", "Snap Tenon"): "زبانه کلیکی",
        ("*", "Rectangular tenon with snap spheres"): "زبانه مستطیلی با گوی‌های کلیکی",
        ("*", "Snap Dovetail"): "دم‌چلچله‌ای کلیکی",
        ("*", "Tapered wedge connector with snap spheres"): "رابط گوه‌ای مخروطی با گوی‌های کلیکی",
        ("*", "Custom Connector"): "رابط سفارشی",
        ("*", "Use another mesh object from the scene as connector shape"): "استفاده از یک شیء مشی دیگر از صحنه به‌عنوان شکل رابط",
        ("*", "Select connector object"): "انتخاب شیء رابط",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "یک شیء مشی از این صحنه که به‌عنوان شکل رابط استفاده می‌شود. محور Z محلی آن جهت درج در نظر گرفته می‌شود؛ بر اساس مقادیر عرض/طول/عمق زیر مقیاس‌دهی خواهد شد.",
        ("*", "Custom Width (mm)"): "عرض سفارشی (mm)",
        ("*", "Target size along the object's local X axis"): "اندازه هدف در امتداد محور X محلی شیء",
        ("*", "Custom Length (mm)"): "طول سفارشی (mm)",
        ("*", "Target size along the object's local Y axis"): "اندازه هدف در امتداد محور Y محلی شیء",
        ("*", "Custom Depth (mm)"): "عمق سفارشی (mm)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "اندازه هدف در امتداد محور Z محلی شیء (عمق درج)",
        ("*", "Please select a connector object for Custom Connector."): "لطفاً یک شیء رابط برای رابط سفارشی انتخاب کنید.",
        ("*", "Selected connector object has no usable mesh data."): "شیء رابط انتخاب‌شده داده مشی قابل‌استفاده‌ای ندارد.",
        ("*", "Base size"): "اندازه پایه",
        ("*", "Dovetail Width (mm)"): "عرض دم‌چلچله‌ای (mm)",
        ("*", "Dovetail Length (mm)"): "طول دم‌چلچله‌ای (mm)",
        ("*", "Length along seam plane (local v)"): "طول در امتداد صفحه درز (v محلی)",
        ("*", "Dovetail Depth (mm)"): "عمق دم‌چلچله‌ای (mm)",
        ("*", "Taper (%)"): "باریک‌شدگی (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "درصدی که نوک نسبت به پایه باریک‌تر است",
        ("*", "Signed Taper (%)"): "باریک‌شدگی علامت‌دار (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "باریک‌شدگی علامت‌دار در امتداد جهت درج. مثبت پهن می‌کند، منفی باریک می‌کند. اگر صفر نباشد، باریک‌شدگی ساده را نادیده می‌گیرد.",
        ("*", "Span Axis"): "محور گستره",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "«خودکار» در امتداد محور عرض دم‌چلچله‌ای کشیده می‌شود و به سمت‌های بیرونی بریده می‌شود؛ X/Y/Z در صورتی که در صفحه درز قرار داشته باشد، کشیدگی را در امتداد آن محور جهانی اجباری می‌کند؛ «هیچ‌کدام» از طول تنظیم‌شده دستی استفاده می‌کند",
        ("*", "None"): "هیچ‌کدام",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "از طول دم‌چلچله‌ای تنظیم‌شده دستی استفاده می‌کند؛ لبه‌ها فقط در صورت فعال بودن برش سخت جانبی بریده می‌شوند",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "به‌طور خودکار در امتداد محور عرض دم‌چلچله‌ای کشیده می‌شود و به سمت‌های بیرونی بریده می‌شود",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "در صورت قرارگیری در صفحه درز، کشیدگی در امتداد محور جهانی X را اجباری می‌کند",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "در صورت قرارگیری در صفحه درز، کشیدگی در امتداد محور جهانی Y را اجباری می‌کند",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "در صورت قرارگیری در صفحه درز، کشیدگی در امتداد محور جهانی Z را اجباری می‌کند",
        ("*", "Forces hard-side cut along this axis."): "برش سخت جانبی را در امتداد این محور اجباری می‌کند.",
        ("*", "Hard-side Cut"): "برش سخت جانبی",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "برش جانبی تیز را برای سوکت/شیار دم‌چلچله‌ای ترجیح می‌دهد",
        ("*", "Margin (%)"): "حاشیه (%)",
        ("*", "Trim percentage at both ends of seam span"): "درصد برش در هر دو انتهای گستره درز",
        ("*", "Placement"): "قرارگیری",
        ("*", "Offset along Width (mm)"): "افست در امتداد عرض (mm)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "افست درون صفحه برش در امتداد محور عرض (u) برای جابه‌جایی الگوی دم‌چلچله‌ای",
        ("*", "Offset along Length (mm)"): "افست در امتداد طول (mm)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "افست درون صفحه برش در امتداد محور طول (v) برای جابه‌جایی الگوی دم‌چلچله‌ای",
        ("*", "Rotation in plane (deg)"): "چرخش درون صفحه (درجه)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "چرخش درون صفحه برش برای جهت‌دهی الگوی دم‌چلچله‌ای",
        ("*", "Span Mode"): "حالت گستره",
        ("*", "How the dovetail spans along the seam"): "نحوه گسترش دم‌چلچله‌ای در امتداد درز",
        ("*", "Auto"): "خودکار",
        ("*", "Use full edge-to-edge span of the seam"): "استفاده از کل گستره درز از لبه تا لبه",
        ("*", "Fixed"): "ثابت",
        ("*", "Use a fixed repeating spacing"): "استفاده از فاصله تکراری ثابت",
        ("*", "Centered"): "مرکزچین",
        ("*", "Center block(s) with margins"): "مرکزچینی بلوک(ها) با حاشیه‌ها",
        ("*", "Live Preview"): "پیش‌نمایش زنده",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "نمایش پیش‌نمایش سیمی زنده از جای‌گذاری رابط‌ها (خط/شبکه) برای انتخاب فعلی. به دلیل کارایی، به ۲۰۰ شیء پیش‌نمایش محدود شده است.",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "پیش‌نمایش زنده رابط‌ها در ۲۰۰ شیء متوقف شد؛ نقاط باقی‌مانده نمایش داده نمی‌شوند.",
        ("*", "Distribution"): "توزیع",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "توزیع رابط‌ها در امتداد یک خط یا در یک شبکه روی سطح درز",
        ("*", "Line"): "خط",
        ("*", "Place connectors along a line in the seam face"): "جای‌گذاری رابط‌ها در امتداد یک خط در سطح درز",
        ("*", "Grid"): "شبکه",
        ("*", "Distribute connectors in a grid over the seam face"): "توزیع رابط‌ها در یک شبکه روی سطح درز",
        ("*", "Connectors per Seam"): "رابط در هر درز",
        ("*", "Rows (GRID)"): "ردیف‌ها (شبکه)",
        ("*", "Number of rows for grid distribution"): "تعداد ردیف‌ها برای توزیع شبکه‌ای",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "حاشیه لبه در امتداد درز (و عمود بر آن در شبکه) به‌صورت درصدی از طول قطعه (توصیه: ۰ تا ۴۰٪)",
        ("*", "Spheres per side"): "گوی در هر سمت",
        ("*", "Number of snap spheres per side/around"): "تعداد گوی‌های کلیکی در هر سمت/اطراف",
        ("*", "Sphere Diameter (mm)"): "قطر گوی (mm)",
        ("*", "Diameter of snap spheres"): "قطر گوی‌های کلیکی",
        ("*", "Protrusion (mm)"): "بیرون‌زدگی (mm)",
        ("*", "How far spheres protrude from side surface"): "میزان بیرون‌زدگی گوی‌ها از سطح جانبی",
        ("*", "Pin Diameter (mm)"): "قطر پین (mm)",
        ("*", "Pin Length (mm)"): "طول پین (mm)",
        ("*", "Segments"): "بخش‌ها",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "بخش‌های شعاعی پین استوانه‌ای (نرمی بصری)",
        ("*", "Tenon Width (mm)"): "عرض زبانه (mm)",
        ("*", "Tenon Depth (mm)"): "عمق زبانه (mm)",
        ("*", "Chamfer (mm)"): "پخ (mm)",
        ("*", "Insert Depth (%)"): "عمق درج (%)",
        ("*", "Percentage of connector length recessed into part A"): "درصدی از طول رابط که در قطعه A فرورفته است",
        ("*", "Material Profiles"): "پروفایل‌های متریال",
        ("*", "Select a material profile to auto-fill tolerance per side"): "یک پروفایل متریال برای پر کردن خودکار تلورانس هر سمت انتخاب کنید",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "تلورانس پیشنهادی هر سمت: {val:.2f} mm",
        ("*", "Tolerance per Face (mm)"): "تلورانس هر وجه (mm)",
        ("*", "Overrides material profile (0 = use profile value)"): "پروفایل متریال را نادیده می‌گیرد (۰ = استفاده از مقدار پروفایل)",
        ("*", "More segmentation settings"): "تنظیمات بیشتر تقسیم‌بندی",
        ("*", "Show advanced segmentation options"): "نمایش گزینه‌های پیشرفته تقسیم‌بندی",
        ("*", "More connection settings"): "تنظیمات بیشتر اتصال",
        ("*", "Show advanced connection/geometry options"): "نمایش گزینه‌های پیشرفته اتصال/هندسه",
        ("*", "More tolerance settings"): "تنظیمات بیشتر تلورانس",
        ("*", "Show advanced tolerance options"): "نمایش گزینه‌های پیشرفته تلورانس",
        ("*", "More alignment settings"): "تنظیمات بیشتر تراز",
        ("*", "Show advanced alignment options"): "نمایش گزینه‌های پیشرفته تراز",
        ("*", "Segmentation"): "تقسیم‌بندی",
        ("*", "Less..."): "کمتر...",
        ("*", "Adjust"): "تنظیم",
        ("*", "Connections"): "اتصالات",
        ("*", "Add connectors"): "افزودن رابط‌ها",
        ("Operator", "Add connectors"): "افزودن رابط‌ها",
        ("*", "Place connectors (click)"): "جای‌گذاری رابط‌ها (کلیک)",
        ("Operator", "Place connectors (click)"): "جای‌گذاری رابط‌ها (کلیک)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "وجوه را در حالت شیء انتخاب کنید (A = هدف، B = متحرک)",
        ("*", "A: none"): "A: هیچ‌کدام",
        ("*", "B: none"): "B: هیچ‌کدام",
        ("*", "Pick Face A"): "انتخاب وجه A",
        ("Operator", "Pick Face A"): "انتخاب وجه A",
        ("*", "Pick Face B"): "انتخاب وجه B",
        ("Operator", "Pick Face B"): "انتخاب وجه B",
        ("*", "Align Faces"): "تراز کردن وجوه",
        ("Operator", "Align Faces"): "تراز کردن وجوه",
    },
    "hi_IN": {
        ("*", "Adjust split axis"): "कट अक्ष समायोजित करें",
        ("Operator", "Adjust split axis"): "कट अक्ष समायोजित करें",
        ("*", "Split axis adjusted."): "कट अक्ष समायोजित किया गया।",
        ("*", "Adjust split axis cancelled."): "कट अक्ष समायोजन रद्द किया गया।",
        ("*", "Planar Split"): "समतल कट",
        ("Operator", "Planar Split"): "समतल कट",
        ("*", "Splitting into many parts can take a while on dense meshes..."): "घने मेश पर कई भागों में विभाजित करने में समय लग सकता है...",
        ("*", "Auto-cap during split did not find valid loops to fill."): "स्वचालित कैपिंग को कोई मान्य लूप नहीं मिला।",
        ("*", "Auto-capped seams on {n} part(s)."): "{n} भाग(ों) पर स्वचालित कैपिंग की गई।",
        ("*", "Fewer parts created than expected ({have} < {want})."): "अपेक्षा से कम भाग बनाए गए ({have} < {want})।",
        ("*", "{n} parts created."): "{n} भाग बनाए गए।",
        ("*", "Cap seams now"): "अभी किनारे बंद करें",
        ("Operator", "Cap seams now"): "अभी किनारे बंद करें",
        ("*", "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred."): "प्रति समतल ठीक दो कट-किनारा लूप (बाहरी+आंतरिक) के बीच भरें। सीड्स को प्राथमिकता दी जाती है।",
        ("*", "Only selected objects"): "केवल चयनित ऑब्जेक्ट",
        ("*", "0 = all planes per object, 1 = only largest"): "0 = प्रति ऑब्जेक्ट सभी समतल, 1 = केवल सबसे बड़ा",
        ("*", "Select only (no fill)"): "केवल चयन करें (भरें नहीं)",
        ("*", "Require exactly two seed edges"): "ठीक दो सीड किनारों की आवश्यकता",
        ("*", "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection)."): "यदि संपादन मोड में ठीक दो किनारे चयनित हैं, तो केवल उन्हें सीड के रूप में उपयोग करें (कोई स्वचालित पहचान नहीं)।",
        ("*", "No mesh objects to cap. Select split parts or use the parts collection."): "बंद करने के लिए कोई मेश ऑब्जेक्ट नहीं। कटे हुए भाग चुनें या भाग संग्रह का उपयोग करें।",
        ("*", "Processing failed on '{name}': {err}"): "'{name}' को संसाधित करना विफल: {err}",
        ("*", "Could not determine split edge loops to select."): "चयन के लिए कट-किनारा लूप निर्धारित नहीं किए जा सके।",
        ("*", "Could not determine and fill split edge loops."): "कट-किनारा लूप निर्धारित और भरे नहीं जा सके।",
        ("*", "Selected split edge loops on {n} object(s)."): "{n} ऑब्जेक्ट(ों) पर कट-किनारा लूप चयनित किए गए।",
        ("*", "Capped seams on {n} object(s)."): "{n} ऑब्जेक्ट(ों) पर किनारे बंद किए गए।",
        ("*", "Please select a mesh object."): "कृपया एक मेश ऑब्जेक्ट चुनें।",
        ("*", "Object has unapplied transforms"): "ऑब्जेक्ट में लागू न किए गए ट्रांसफ़ॉर्म हैं",
        ("*", "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."): "सटीक और पूर्वानुमानित परिणामों के लिए सभी ट्रांसफ़ॉर्म लागू करने पर विचार करें (Ctrl+A)।",
        ("*", "Split Offset (mm)"): "कट ऑफ़सेट (मिमी)",
        ("*", "Offset of the cutting plane along the split axis (positive in axis direction)"): "विभाजन अक्ष के साथ कट समतल का ऑफ़सेट (अक्ष दिशा में धनात्मक)",
        ("*", "Split Axis"): "विभाजन अक्ष",
        ("*", "Split along X"): "X के साथ विभाजित करें",
        ("*", "Split along Y"): "Y के साथ विभाजित करें",
        ("*", "Split along Z"): "Z के साथ विभाजित करें",
        ("*", "Show split preview"): "विभाजन पूर्वावलोकन दिखाएँ",
        ("*", "Show temporary orange planes at planned cut positions"): "नियोजित कट स्थानों पर अस्थायी नारंगी समतल दिखाएँ",
        ("*", "Number of Parts"): "भागों की संख्या",
        ("*", "Number of desired segments (cut planes = parts - 1)"): "वांछित खंडों की संख्या (कट समतल = भाग - 1)",
        ("*", "Cap seams during split"): "विभाजन के दौरान सीम बंद करें",
        ("*", "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."): "कटिंग के बाद स्वचालित रूप से सीम बंद करें। कैविटी/आंतरिक शेल के साथ: बाहरी/आंतरिक लूप का सटीक भरना; कैविटी के बिना: सरल भरना। इससे रन-टाइम बढ़ सकता है।",
        ("*", "Connector Type"): "कनेक्टर प्रकार",
        ("*", "Cylinder Pin"): "बेलनाकार पिन",
        ("*", "Dowel pin + socket"): "पिन + सॉकेट",
        ("*", "Rectangular Tenon"): "आयताकार टेनन",
        ("*", "Anti-rotation joint"): "घूर्णन-रोधी जोड़",
        ("*", "Dovetail"): "डवटेल",
        ("*", "Tapered wedge connector"): "शंक्वाकार वेज कनेक्टर",
        ("*", "Snap Pin"): "स्नैप पिन",
        ("*", "Connector with snap spheres"): "स्नैप बॉल्स वाला कनेक्टर",
        ("*", "Snap Tenon"): "स्नैप टेनन",
        ("*", "Rectangular tenon with snap spheres"): "स्नैप बॉल्स के साथ आयताकार टेनन",
        ("*", "Snap Dovetail"): "स्नैप डवटेल",
        ("*", "Tapered wedge connector with snap spheres"): "स्नैप बॉल्स के साथ शंक्वाकार वेज कनेक्टर",
        ("*", "Custom Connector"): "कस्टम कनेक्टर",
        ("*", "Use another mesh object from the scene as connector shape"): "दृश्य से किसी अन्य मेश ऑब्जेक्ट को कनेक्टर आकार के रूप में उपयोग करें",
        ("*", "Select connector object"): "कनेक्टर ऑब्जेक्ट चुनें",
        ("*", "Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below."): "इस दृश्य से एक मेश ऑब्जेक्ट, जिसे कनेक्टर आकार के रूप में उपयोग किया जाता है। इसकी स्थानीय Z-अक्ष को सम्मिलन दिशा माना जाता है; इसे नीचे दिए गए चौड़ाई/लंबाई/गहराई मानों के अनुसार स्केल किया जाएगा।",
        ("*", "Custom Width (mm)"): "कस्टम चौड़ाई (मिमी)",
        ("*", "Target size along the object's local X axis"): "ऑब्जेक्ट के स्थानीय X-अक्ष के साथ लक्ष्य आकार",
        ("*", "Custom Length (mm)"): "कस्टम लंबाई (मिमी)",
        ("*", "Target size along the object's local Y axis"): "ऑब्जेक्ट के स्थानीय Y-अक्ष के साथ लक्ष्य आकार",
        ("*", "Custom Depth (mm)"): "कस्टम गहराई (मिमी)",
        ("*", "Target size along the object's local Z axis (insertion depth)"): "ऑब्जेक्ट के स्थानीय Z-अक्ष के साथ लक्ष्य आकार (सम्मिलन गहराई)",
        ("*", "Please select a connector object for Custom Connector."): "कस्टम कनेक्टर के लिए एक कनेक्टर ऑब्जेक्ट चुनें।",
        ("*", "Selected connector object has no usable mesh data."): "चयनित कनेक्टर ऑब्जेक्ट में उपयोग योग्य मेश डेटा नहीं है।",
        ("*", "Base size"): "आधार आकार",
        ("*", "Dovetail Width (mm)"): "डवटेल चौड़ाई (मिमी)",
        ("*", "Dovetail Length (mm)"): "डवटेल लंबाई (मिमी)",
        ("*", "Length along seam plane (local v)"): "सीम समतल के साथ लंबाई (स्थानीय v)",
        ("*", "Dovetail Depth (mm)"): "डवटेल गहराई (मिमी)",
        ("*", "Taper (%)"): "टेपर (%)",
        ("*", "Percentage by which the tip is narrower than the base"): "प्रतिशत जिससे नोक आधार से संकरी है",
        ("*", "Signed Taper (%)"): "साइन किया गया टेपर (%)",
        ("*", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."): "सम्मिलन दिशा के साथ साइन किया गया टेपर। धनात्मक चौड़ा करता है, ऋणात्मक संकरा करता है। यदि शून्य नहीं है, तो यह सरल टेपर को ओवरराइड करता है।",
        ("*", "Span Axis"): "स्पैन अक्ष",
        ("*", "Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length"): "'स्वचालित' डवटेल की चौड़ाई अक्ष के साथ फैलता है और बाहरी किनारों तक काटता है; X/Y/Z उस विश्व अक्ष के साथ विस्तार को बाध्य करता है यदि वह सीम समतल में स्थित हो; 'कोई नहीं' मैन्युअल रूप से सेट लंबाई का उपयोग करता है",
        ("*", "None"): "कोई नहीं",
        ("*", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled"): "मैन्युअल रूप से सेट डवटेल लंबाई का उपयोग करता है; किनारों को केवल तभी काटता है जब हार्ड साइड कट सक्षम हो",
        ("*", "Automatically stretch along the Dovetail Width axis and trim to the outer sides"): "स्वचालित रूप से डवटेल की चौड़ाई अक्ष के साथ फैलता है और बाहरी किनारों तक काटता है",
        ("*", "Force overshoot along world X, if it lies in the seam plane"): "यदि सीम समतल में स्थित हो तो विश्व X-अक्ष के साथ विस्तार को बाध्य करता है",
        ("*", "Force overshoot along world Y, if it lies in the seam plane"): "यदि सीम समतल में स्थित हो तो विश्व Y-अक्ष के साथ विस्तार को बाध्य करता है",
        ("*", "Force overshoot along world Z, if it lies in the seam plane"): "यदि सीम समतल में स्थित हो तो विश्व Z-अक्ष के साथ विस्तार को बाध्य करता है",
        ("*", "Forces hard-side cut along this axis."): "इस अक्ष के साथ हार्ड साइड कट को बाध्य करता है।",
        ("*", "Hard-side Cut"): "हार्ड साइड कट",
        ("*", "Prefer sharp side cut for dovetail socket/slot"): "डवटेल सॉकेट/खांचे के लिए एक तीक्ष्ण साइड कट को प्राथमिकता देता है",
        ("*", "Margin (%)"): "मार्जिन (%)",
        ("*", "Trim percentage at both ends of seam span"): "सीम स्पैन के दोनों सिरों पर काटने का प्रतिशत",
        ("*", "Placement"): "स्थिति",
        ("*", "Offset along Width (mm)"): "चौड़ाई के साथ ऑफ़सेट (मिमी)",
        ("*", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"): "डवटेल पैटर्न को खिसकाने के लिए कट समतल के भीतर चौड़ाई अक्ष (u) के साथ ऑफ़सेट",
        ("*", "Offset along Length (mm)"): "लंबाई के साथ ऑफ़सेट (मिमी)",
        ("*", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"): "डवटेल पैटर्न को खिसकाने के लिए कट समतल के भीतर लंबाई अक्ष (v) के साथ ऑफ़सेट",
        ("*", "Rotation in plane (deg)"): "समतल में घूर्णन (डिग्री)",
        ("*", "Rotation within the cut plane to orient the dovetail pattern"): "डवटेल पैटर्न को उन्मुख करने के लिए कट समतल के भीतर घूर्णन",
        ("*", "Span Mode"): "स्पैन मोड",
        ("*", "How the dovetail spans along the seam"): "डवटेल सीम के साथ कैसे फैलता है",
        ("*", "Auto"): "स्वचालित",
        ("*", "Use full edge-to-edge span of the seam"): "सीम का पूर्ण किनारे-से-किनारे स्पैन उपयोग करें",
        ("*", "Fixed"): "स्थिर",
        ("*", "Use a fixed repeating spacing"): "एक स्थिर दोहराव अंतराल का उपयोग करें",
        ("*", "Centered"): "केंद्रित",
        ("*", "Center block(s) with margins"): "मार्जिन के साथ ब्लॉक(ओं) को केंद्रित करें",
        ("*", "Live Preview"): "लाइव पूर्वावलोकन",
        ("*", "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."): "वर्तमान चयन के लिए कनेक्टर प्लेसमेंट (लाइन/ग्रिड) का लाइव वायरफ़्रेम पूर्वावलोकन दिखाएँ। प्रदर्शन के लिए 200 पूर्वावलोकन ऑब्जेक्ट तक सीमित।",
        ("*", "Connector live preview stopped at 200 objects; remaining points are not shown."): "कनेक्टर लाइव पूर्वावलोकन 200 ऑब्जेक्ट पर रुक गया; शेष बिंदु नहीं दिखाए गए हैं।",
        ("*", "Distribution"): "वितरण",
        ("*", "Distribute connectors along a line or a grid across the seam face"): "सीम फेस पर एक रेखा या ग्रिड के साथ कनेक्टर वितरित करें",
        ("*", "Line"): "रेखा",
        ("*", "Place connectors along a line in the seam face"): "सीम फेस में एक रेखा के साथ कनेक्टर रखें",
        ("*", "Grid"): "ग्रिड",
        ("*", "Distribute connectors in a grid over the seam face"): "सीम फेस पर एक ग्रिड में कनेक्टर वितरित करें",
        ("*", "Connectors per Seam"): "प्रति सीम कनेक्टर",
        ("*", "Rows (GRID)"): "पंक्तियाँ (ग्रिड)",
        ("*", "Number of rows for grid distribution"): "ग्रिड वितरण के लिए पंक्तियों की संख्या",
        ("*", "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"): "भाग की लंबाई के प्रतिशत के रूप में सीम (और ग्रिड में लंबवत) के साथ किनारे का मार्जिन (0-40% अनुशंसित)",
        ("*", "Spheres per side"): "प्रति साइड गोले",
        ("*", "Number of snap spheres per side/around"): "प्रति साइड/चारों ओर स्नैप गोलों की संख्या",
        ("*", "Sphere Diameter (mm)"): "गोला व्यास (मिमी)",
        ("*", "Diameter of snap spheres"): "स्नैप गोलों का व्यास",
        ("*", "Protrusion (mm)"): "प्रोट्रूज़न (मिमी)",
        ("*", "How far spheres protrude from side surface"): "गोले साइड सतह से कितना बाहर निकलते हैं",
        ("*", "Pin Diameter (mm)"): "पिन व्यास (मिमी)",
        ("*", "Pin Length (mm)"): "पिन लंबाई (मिमी)",
        ("*", "Segments"): "खंड",
        ("*", "Cylinder pin radial segments (visual smoothness)"): "बेलनाकार पिन के रेडियल खंड (दृश्य चिकनाई)",
        ("*", "Tenon Width (mm)"): "टेनन चौड़ाई (मिमी)",
        ("*", "Tenon Depth (mm)"): "टेनन गहराई (मिमी)",
        ("*", "Chamfer (mm)"): "चम्फर (मिमी)",
        ("*", "Insert Depth (%)"): "सम्मिलन गहराई (%)",
        ("*", "Percentage of connector length recessed into part A"): "भाग A में धँसे कनेक्टर की लंबाई का प्रतिशत",
        ("*", "Material Profiles"): "सामग्री प्रोफ़ाइल",
        ("*", "Select a material profile to auto-fill tolerance per side"): "प्रति साइड सहनशीलता को स्वतः भरने के लिए एक सामग्री प्रोफ़ाइल चुनें",
        ("*", "Recommended tolerance per side: {val:.2f} mm"): "अनुशंसित सहनशीलता प्रति साइड: {val:.2f} मिमी",
        ("*", "Tolerance per Face (mm)"): "प्रति फेस सहनशीलता (मिमी)",
        ("*", "Overrides material profile (0 = use profile value)"): "सामग्री प्रोफ़ाइल को ओवरराइड करता है (0 = प्रोफ़ाइल मान का उपयोग करें)",
        ("*", "More segmentation settings"): "अधिक विभाजन सेटिंग्स",
        ("*", "Show advanced segmentation options"): "उन्नत विभाजन विकल्प दिखाएँ",
        ("*", "More connection settings"): "अधिक कनेक्शन सेटिंग्स",
        ("*", "Show advanced connection/geometry options"): "उन्नत कनेक्शन/ज्यामिति विकल्प दिखाएँ",
        ("*", "More tolerance settings"): "अधिक सहनशीलता सेटिंग्स",
        ("*", "Show advanced tolerance options"): "उन्नत सहनशीलता विकल्प दिखाएँ",
        ("*", "More alignment settings"): "अधिक संरेखण सेटिंग्स",
        ("*", "Show advanced alignment options"): "उन्नत संरेखण विकल्प दिखाएँ",
        ("*", "Segmentation"): "विभाजन",
        ("*", "Less..."): "कम...",
        ("*", "Adjust"): "समायोजित करें",
        ("*", "Connections"): "कनेक्शन",
        ("*", "Add connectors"): "कनेक्टर जोड़ें",
        ("Operator", "Add connectors"): "कनेक्टर जोड़ें",
        ("*", "Place connectors (click)"): "कनेक्टर रखें (क्लिक)",
        ("Operator", "Place connectors (click)"): "कनेक्टर रखें (क्लिक)",
        ("*", "Pick faces in Object Mode (A = target, B = moving)"): "ऑब्जेक्ट मोड में फेस चुनें (A = लक्ष्य, B = चलने योग्य)",
        ("*", "A: none"): "A: कोई नहीं",
        ("*", "B: none"): "B: कोई नहीं",
        ("*", "Pick Face A"): "फेस A चुनें",
        ("Operator", "Pick Face A"): "फेस A चुनें",
        ("*", "Pick Face B"): "फेस B चुनें",
        ("Operator", "Pick Face B"): "फेस B चुनें",
        ("*", "Align Faces"): "फेस संरेखित करें",
        ("Operator", "Align Faces"): "फेस संरेखित करें",
    },
}
```

---

### ops_align.py

```py
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# ops_align.py

import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector, Matrix
from bpy_extras import view3d_utils

from .utils import report_user
from .utils import _trf

_FACE_TO_FACE_LOCAL_FLIP = True


# ---------------------------
# Raycast and math utilities
# ---------------------------

def _raycast_pick_face(context, event):
    """
    Raycast from mouse cursor to get (obj, hit_position, hit_normal_world, face_index) for mesh faces.
    Returns None if no face is hit or not in a 3D View.
    """
    if context.space_data is None or context.space_data.type != 'VIEW_3D':
        return None

    region = context.region
    rv3d = context.space_data.region_3d
    co2d = Vector((event.mouse_region_x, event.mouse_region_y))

    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d)
    ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d).normalized()

    depsgraph = context.evaluated_depsgraph_get()
    scene = context.scene

    hit, loc, norm, face_index, obj, _ = scene.ray_cast(depsgraph, ray_origin, ray_dir, distance=1e6)
    if not hit or not obj or obj.type != 'MESH' or face_index < 0:
        return None

    # norm from scene.ray_cast is already world-space
    return obj, loc, norm.normalized(), face_index


def _object_face_frame_world(obj, face_index):
    """
    Compute a stable face frame in world space:
    - z_world: face normal (world)
    - x_world: robust in-plane tangent from averaged projected edges; fallback projects a world axis
    - y_world: z x x (right-handed)
    """
    me = obj.data
    if face_index < 0 or face_index >= len(me.polygons):
        raise ValueError("Invalid face index")
    poly = me.polygons[face_index]

    origin = obj.matrix_world @ poly.center

    # Normal (world) via inverse-transpose
    n_local = poly.normal
    N = obj.matrix_world.to_3x3().inverted().transposed()
    z_world = (N @ n_local).normalized()

    Mw3 = obj.matrix_world.to_3x3()

    # Robust tangent: average all edge directions projected into the face plane
    verts = me.vertices
    idxs = poly.vertices
    tan = Vector((0.0, 0.0, 0.0))
    for i in range(len(idxs)):
        v0 = verts[idxs[i]].co
        v1 = verts[(idxs[(i + 1) % len(idxs)])].co
        e = Mw3 @ (v1 - v0)
        e_proj = e - e.dot(z_world) * z_world
        if e_proj.length_squared > 1e-16:
            tan += e_proj.normalized()

    if tan.length_squared <= 1e-16:
        # Fallback: project world +X (or +Y if near parallel) into plane
        ref = Vector((1, 0, 0))
        if abs(ref.dot(z_world)) > 0.9:
            ref = Vector((0, 1, 0))
        tan = (ref - ref.dot(z_world) * z_world)

    x_world = tan.normalized()
    y_world = z_world.cross(x_world).normalized()
    x_world = y_world.cross(z_world).normalized()

    R = Matrix((x_world, y_world, z_world)).transposed()  # columns as axes
    return origin, R


def _make_frame_matrix(origin, R):
    """Build a 4x4 matrix from origin and a 3x3 rotation/axes matrix."""
    M = Matrix.Identity(4)
    M[0][0], M[0][1], M[0][2] = R[0][0], R[0][1], R[0][2]
    M[1][0], M[1][1], M[1][2] = R[1][0], R[1][1], R[1][2]
    M[2][0], M[2][1], M[2][2] = R[2][0], R[2][1], R[2][2]
    M.translation = origin
    return M


# ---------------------------
# Selection helpers (RNA / BMesh only, no selection operators)
# ---------------------------

def _deselect_all_objects():
    """Deselect all objects of the current view layer via RNA (replaces bpy.ops.object.select_all)."""
    try:
        for o in list(bpy.context.view_layer.objects):
            try:
                # select_set() can raise for objects that cannot be selected (e.g. hidden); ignore
                o.select_set(False)
            except Exception:
                pass
    except Exception:
        pass


def _bm_clear_selection(bm):
    """Deselect every vertex, edge and face of an edit BMesh (replaces bpy.ops.mesh.select_all)."""
    for f in bm.faces:
        f.select_set(False)
    for e in bm.edges:
        e.select_set(False)
    for v in bm.verts:
        v.select_set(False)
    try:
        bm.select_history.clear()
    except Exception:
        pass


def _edit_bmesh_deselect_all(obj):
    """Deselect all elements of obj's live edit BMesh and flush to the viewport.

    Returns True on success, False if obj is not in Edit Mode or BMesh access failed.
    """
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        return False
    try:
        bm = bmesh.from_edit_mesh(obj.data)
        # Keep the BMesh itself in face select mode (matches the tool setting)
        bm.select_mode = {'FACE'}
        _bm_clear_selection(bm)
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return True
    except Exception:
        return False


def _set_face_select_mode_tool_setting():
    """Set FACE select mode via tool settings (must happen BEFORE entering Edit Mode)."""
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    except Exception:
        pass


# ---------------------------
# Highlight utilities (persistent until alignment) — BMesh based
# ---------------------------

def _ensure_multi_object_edit(obj_list):
    """
    Ensure all provided mesh objects are selected and in Edit Mode together,
    set face select mode, and clear edit selection so the next face selection is visible.
    """
    if not obj_list:
        return

    objs = [o for o in dict.fromkeys(obj_list) if o and o.type == 'MESH']
    if not objs:
        return

    view_layer = bpy.context.view_layer

    # Deselect all objects (RNA), then select targets
    _deselect_all_objects()
    for o in objs:
        try:
            o.select_set(True)
        except Exception:
            pass

    # Set an active object
    try:
        view_layer.objects.active = objs[0]
    except Exception:
        pass

    # Face select mode through tool settings; the edit mesh is created with this mode,
    # so bpy.ops.mesh.select_mode(type='FACE') is no longer needed.
    _set_face_select_mode_tool_setting()

    # Enter Edit Mode (multi-object). No public non-operator equivalent exists.
    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except Exception:
        return

    # Clear existing edit selection on every edit mesh (replaces mesh.select_all DESELECT,
    # which only worked on the meshes the operator context happened to cover).
    for o in objs:
        _edit_bmesh_deselect_all(o)


def _select_single_face(obj, face_index):
    """
    Select only the specified face on obj using the live Edit BMesh and flush immediately.
    Ensures obj is the active edit object while changing its selection so the viewport shows orange.
    """
    if not obj or obj.type != 'MESH' or face_index < 0:
        return
    me = obj.data
    if not (0 <= face_index < len(me.polygons)):
        return

    view_layer = bpy.context.view_layer
    prev_active = view_layer.objects.active

    # 1) Make obj active and ensure we're in Edit Mode (multi-object edit supported)
    try:
        obj.select_set(True)
        view_layer.objects.active = obj
    except Exception:
        pass
    if obj.mode != 'EDIT':
        _set_face_select_mode_tool_setting()
        try:
            bpy.ops.object.mode_set(mode='EDIT')
        except Exception:
            return

    # 2) Operate directly on the live edit BMesh (obj is in Edit Mode here)
    try:
        bm = bmesh.from_edit_mesh(me)
    except Exception:
        # No BMesh available: nothing sensible left to do without selection operators
        return

    # Face select mode on the BMesh itself (replaces bpy.ops.mesh.select_mode(type='FACE'))
    bm.select_mode = {'FACE'}

    # Lookup tables are required for index access on BMesh sequences
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Clear selection on this mesh, then select target face
    _bm_clear_selection(bm)

    bm_face = None
    try:
        bm_face = bm.faces[face_index]
    except Exception:
        # Fallback: match by vertex index set (only valid while topology is unchanged)
        bm.verts.index_update()
        poly_verts = set(me.polygons[face_index].vertices)
        for f in bm.faces:
            if set(v.index for v in f.verts) == poly_verts:
                bm_face = f
                break
    if bm_face is None:
        return

    # select_set(True) also selects the face's edges and vertices
    bm_face.select_set(True)

    # 3) Flush to viewport (replaces the old EDGE/FACE select_mode toggle trick)
    bm.select_flush_mode()
    try:
        bmesh.update_edit_mesh(me, loop_triangles=False, destructive=False)
    except Exception:
        try:
            me.update()
        except Exception:
            pass

    # 4) Optionally restore previous active edit object if it differs
    try:
        if prev_active and prev_active != obj and prev_active.type == 'MESH' and prev_active.select_get():
            view_layer.objects.active = prev_active
    except Exception:
        pass


def _highlight_picked_face_persistent(objA, idxA, objB=None, idxB=-1):
    """
    Keep highlights for A (and optionally B) by ensuring both are in multi-object Edit Mode
    and their faces are selected. Call this after each pick.
    """
    objs = [objA] + ([objB] if (objB and objB != objA) else [])
    _ensure_multi_object_edit(objs)

    # Re-assert selections (entering Edit Mode can clear selection)
    _select_single_face(objA, idxA)
    if objB and objB != objA and idxB >= 0:
        _select_single_face(objB, idxB)

# ---------------------------
# Pick storage (PropertyGroup on WindowManager)
# ---------------------------

class SNAP_PG_picks(bpy.types.PropertyGroup):
    """Stores the picked Face A (target) and Face B (moving) for the align tool."""

    face_a_obj: bpy.props.StringProperty(name='Face A Object')
    face_a_index: bpy.props.IntProperty(name='Face A Index', default=-1)
    face_b_obj: bpy.props.StringProperty(name='Face B Object')
    face_b_index: bpy.props.IntProperty(name='Face B Index', default=-1)


# ---------------------------
# Modal pick operators (Object Mode, normal cursor)
# ---------------------------

class SNAP_OT_pick_face_a(Operator):
    """Pick target face (A) in Object Mode"""
    bl_idname = "snapsplit.pick_face_a"
    bl_label = "Pick Face A"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        'Canceled.')
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            'No face hit. Orbit/zoom and click directly on a visible mesh.')
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            picks = context.window_manager.snapsplit_picks
            picks.face_a_obj = obj.name
            picks.face_a_index = fidx

            # If B already exists, keep both highlighted; else highlight only A
            nameB = picks.face_b_obj
            idxB = picks.face_b_index
            objB = bpy.data.objects.get(nameB) if nameB else None


            _highlight_picked_face_persistent(objA=obj, idxA=fidx, objB=objB, idxB=idxB)

            # Make B the active object if it exists (guarded: never set active to None)
            try:
                if objB is not None:
                    context.view_layer.objects.active = objB
            except Exception:
                pass

            report_user(self, 'INFO',
                        _trf('Picked A: {name} face {fidx}', name=obj.name, fidx=fidx))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        'Run in a 3D View.')
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SNAP_OT_pick_face_b(Operator):
    """Pick moving face (B) in Object Mode"""
    bl_idname = "snapsplit.pick_face_b"
    bl_label = "Pick Face B"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        'Canceled.')
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            'No face hit. Orbit/zoom and click directly on a visible mesh.')
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            picks = context.window_manager.snapsplit_picks
            picks.face_b_obj = obj.name
            picks.face_b_index = fidx

            # If A already exists, keep both highlighted; else highlight only B
            nameA = picks.face_a_obj
            idxA = picks.face_a_index
            objA = bpy.data.objects.get(nameA) if nameA else None


            _highlight_picked_face_persistent(objA=(objA or obj), idxA=(idxA if objA else fidx),
                                              objB=(obj if objA else None), idxB=(fidx if objA else -1))

            report_user(self, 'INFO',
                        _trf('Picked B: {name} face {fidx}', name=obj.name, fidx=fidx))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        'Run in a 3D View.')
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# ---------------------------
# Clear Picks helpers
# ---------------------------

def _exit_to_object_mode_safe():
    """Try to return to OBJECT mode ignoring errors."""
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass


def _deselect_edit_mesh(obj):
    """Deselect all elements of obj's mesh (works in Edit Mode and in Object Mode).

    - Edit Mode:   live edit BMesh (replaces bpy.ops.mesh.select_all).
    - Object Mode: mesh data select flags through foreach_set, no mode switch needed.
    - If the RNA route is unavailable, enter Edit Mode and use the BMesh route.
    """
    if not obj or obj.type != 'MESH':
        return

    try:
        bpy.context.view_layer.objects.active = obj
    except Exception:
        pass

    # Edit Mode: use the live BMesh
    if obj.mode == 'EDIT':
        _edit_bmesh_deselect_all(obj)
        return

    # Object Mode: write select flags directly into the mesh data
    me = obj.data
    try:
        me.vertices.foreach_set("select", [False] * len(me.vertices))
        me.edges.foreach_set("select", [False] * len(me.edges))
        me.polygons.foreach_set("select", [False] * len(me.polygons))
        me.update()
        return
    except Exception:
        pass

    # Fallback: go through Edit Mode and the BMesh route
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        _edit_bmesh_deselect_all(obj)
    except Exception:
        pass


# ---------------------------
# Align operator (Object Mode driving transform)
# ---------------------------

class SNAP_OT_align_faces(Operator):
    """Align moving face B to target face A (face-to-face, centers matched)"""
    bl_idname = "snapsplit.align_faces"
    bl_label = "Align Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        picks = context.window_manager.snapsplit_picks
        nameA = picks.face_a_obj
        idxA = picks.face_a_index
        nameB = picks.face_b_obj
        idxB = picks.face_b_index


        if not nameA or idxA < 0 or not nameB or idxB < 0:
            report_user(self, 'ERROR',
                        'Pick Face A and Face B first (Object Mode).')
            return {'CANCELLED'}

        objA = bpy.data.objects.get(nameA)
        objB = bpy.data.objects.get(nameB)
        if not objA or not objB or objA.type != 'MESH' or objB.type != 'MESH':
            report_user(self, 'ERROR',
                        'Stored faces not found or not meshes.')
            return {'CANCELLED'}

        # Leave Edit Mode first (the persistent highlight keeps objects in Edit Mode).
        # Leaving flushes the face selection into the mesh data, so the highlight stays
        # visible, and the frame computation below reads up-to-date mesh data.
        _exit_to_object_mode_safe()

        try:
            originA, RA = _object_face_frame_world(objA, idxA)
            originB, RB = _object_face_frame_world(objB, idxB)

        except Exception as e:
            report_user(self, 'ERROR',
                _trf('Could not compute face frames: {error}', error=e))
            return {'CANCELLED'}

        # Face-to-face: flip B's frame by 180 degrees to keep it right-handed
        if _FACE_TO_FACE_LOCAL_FLIP:
            # Columns of RB are the face axes (x, y, z). Negating the Y and Z COLUMNS is a
            # local 180 degree rotation about the face X axis, so B's normal ends up
            # opposite to A's normal for any orientation.
            RB_ff = RB @ Matrix.Diagonal(Vector((1.0, -1.0, -1.0)))
        else:
            # Previous behaviour: negates the ROWS (world components). Only correct for some
            # orientations (e.g. normals along +/-Z). Kept for A/B comparison testing.
            RB_ff = Matrix((RB[0], -RB[1], -RB[2]))

        FA = _make_frame_matrix(originA, RA)
        FB = _make_frame_matrix(originB, RB_ff)

        try:
            M_align = FA @ FB.inverted()
        except Exception:
            report_user(self, 'ERROR',
                        'Alignment transform invalid (singular frame).')
            return {'CANCELLED'}

        # Apply to moving object B
        objB.matrix_world = M_align @ objB.matrix_world

        # Remember the seam plane of this alignment (world space) so that connectors can be
        # placed on slanted seams later. The data is validated against the real vertices
        # before every use, so stale values (parts moved afterwards) are simply ignored.
        # The sign of the normal does not matter: the consumer orients it itself.
        try:
            nA = RA.col[2].to_3d().normalized()   # normal of face A
            xA = RA.col[0].to_3d().normalized()   # stable tangent of face A
            objB["snapsplit_seam_origin"] = [float(originA[0]), float(originA[1]), float(originA[2])]
            objB["snapsplit_seam_normal"] = [float(nA[0]), float(nA[1]), float(nA[2])]
            objB["snapsplit_seam_xdir"] = [float(xA[0]), float(xA[1]), float(xA[2])]
            objB["snapsplit_seam_partner"] = objA.name
            print(f"[SnapSplit] seam stored on '{objB.name}': normal={tuple(round(c, 4) for c in nA)}")
        except Exception as ex:
            print(f"[SnapSplit] could not store seam data: {ex}")


        try:
            objB.data.validate(); objB.data.update()
        except Exception:
            pass

        report_user(self, 'INFO',
                    _trf('Aligned {name} to {name2}.', name=objB.name, name2=objA.name))
        return {'FINISHED'}


# ---------------------------
# Clear Picks operator
# ---------------------------

class SNAP_OT_clear_picks(bpy.types.Operator):
    """Clear stored Face A/B picks and remove their highlights."""
    bl_idname = "snapsplit.clear_picks"
    bl_label = "Clear Picks"
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        picks = context.window_manager.snapsplit_picks

        # Buffer names before clearing, so we can remove highlights
        nameA = picks.face_a_obj
        nameB = picks.face_b_obj
        objA = bpy.data.objects.get(nameA) if nameA else None
        objB = bpy.data.objects.get(nameB) if nameB else None

        # remove the highlight selection (Edit Mode: BMesh, Object Mode: mesh data)
        if objA:
            _deselect_edit_mesh(objA)
        if objB and objB is not objA:
            _deselect_edit_mesh(objB)

        # go back to Object Mode
        _exit_to_object_mode_safe()

        # Reset the stored picks
        picks.face_a_obj = ""
        picks.face_a_index = -1
        picks.face_b_obj = ""
        picks.face_b_index = -1

        self.report({'INFO'}, 'Picks cleared')
        return {'FINISHED'}


classes = (
    SNAP_PG_picks,          # PropertyGroup must be registered before the operators and the pointer
    SNAP_OT_pick_face_a,
    SNAP_OT_pick_face_b,
    SNAP_OT_align_faces,
    SNAP_OT_clear_picks,
)


def register():
    """Register classes and attach the pick storage to bpy.types.WindowManager."""
    # Labels are plain class attributes; Blender translates them itself.
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.snapsplit_picks = bpy.props.PointerProperty(type=SNAP_PG_picks)


def unregister():
    """Detach the pick storage from bpy.types.WindowManager and unregister all classes."""
    # Remove the pointer first, then the PropertyGroup it references
    if hasattr(bpy.types.WindowManager, "snapsplit_picks"):
        del bpy.types.WindowManager.snapsplit_picks
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
```

---

### ops_connectors.py

```py
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# ops_connectors.py


import bpy
import bmesh
from math import tan, radians
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy_extras import view3d_utils

from .utils import ensure_collection, unit_mm, report_user, apply_modifier_data
from .ops_split import warn_if_unapplied_transforms
from .utils import _trf
from .utils import xray_acquire, xray_release
from .seam_data import (
    SeamValidationError,
    has_freehand_metadata,
    resolve_freehand_plane,
)
from .contact_geometry import resolve_current_contact






# ---------------------------
# Collection cleanup utilities
# ---------------------------

def remove_collection_by_name(coll_name: str):
    """Unlink and remove a collection by name, including unlinking/removing all its objects."""
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        return
    objs = list(coll.objects)
    for obj in objs:
        if not obj:
            continue
        # Unlink object from all collections first
        try:
            for c in list(obj.users_collection):
                try:
                    c.objects.unlink(obj)
                except Exception:
                    pass
        except Exception:
            pass

        mesh_data = getattr(obj, "data", None)
        # Remove object, try hard fallback
        try:
            bpy.data.objects.remove(obj)
        except Exception:
            try:
                _dispose_object(obj, remove_data=False)
            except Exception:
                pass

        # Remove orphaned mesh data
        try:
            if mesh_data and hasattr(mesh_data, "users") and mesh_data.users == 0:
                if mesh_data.__class__.__name__ == "Mesh":
                    bpy.data.meshes.remove(mesh_data)
                else:
                    try:
                        bpy.data.batch_remove((mesh_data,))
                    except Exception:
                        pass
        except Exception:
            pass

    # Unlink the collection from any parents and the scene root
    try:
        for parent in list(bpy.data.collections):
            try:
                if coll.name in [c.name for c in getattr(parent, "children", [])]:
                    parent.children.unlink(coll)
            except Exception:
                pass
    except Exception:
        pass
    try:
        scene_root = bpy.context.view_layer.layer_collection.collection
        if coll.name in [c.name for c in scene_root.children]:
            scene_root.children.unlink(coll)
    except Exception:
        pass
    # Remove collection
    try:
        bpy.data.collections.remove(coll)
    except Exception:
        pass


def remove_cutters_collection():
    """Remove the helper collection '_SnapSplit_Cutters' and its content completely."""
    remove_collection_by_name("_SnapSplit_Cutters")


# ---------------------------
# Live preview (LINE/GRID connector placement) — cleanup
# ---------------------------

# Dedicated name prefix so this preview system never collides with the
# click-placement preview ("SnapSplit_Preview_*") or the split-plane preview
# ("_SnapSplit_PreviewPlane_*"). Sphere rings reuse the same prefix with an
# extra "_Ring_" segment so a single startswith() check in cleanup covers both.
AUTOPREVIEW_PREFIX = "SnapSplit_AutoPreview_"
AUTOPREVIEW_CAP = 200

# Module-level flag so the cap warning is reported only once per "session"
# of being at/above the cap, instead of spamming on every property tweak
# while the preview keeps rebuilding.
_connector_preview_cap_warned = False


def _clear_connector_placement_preview():
    """Remove all connector live-preview objects (wireframe shapes + sphere
    rings) created by update_connector_placement_preview(). Only touches
    objects named with AUTOPREVIEW_PREFIX, so other preview systems sharing
    the same '_SnapSplit_Preview' collection (click-placement preview,
    split-plane preview) are never affected.
    """
    try:
        for o in [o for o in bpy.data.objects if o.name.startswith(AUTOPREVIEW_PREFIX)]:
            mesh_data = getattr(o, "data", None)
            for coll in list(o.users_collection):
                try:
                    coll.objects.unlink(o)
                except Exception:
                    pass
            try:
                bpy.data.objects.remove(o)
            except Exception:
                pass
            try:
                if mesh_data and hasattr(mesh_data, "users") and mesh_data.users == 0:
                    if mesh_data.__class__.__name__ == "Mesh":
                        bpy.data.meshes.remove(mesh_data)
            except Exception:
                pass
    except Exception:
        pass

    # Drop the shared preview collection only if it is now truly empty, so
    # objects from other preview systems (e.g. an active click-placement
    # modal) are never removed by this cleanup pass.
    try:
        pc = bpy.data.collections.get("_SnapSplit_Preview")
        if pc and len(pc.objects) == 0:
            for sc in bpy.data.scenes:
                try:
                    if pc in sc.collection.children:
                        sc.collection.children.unlink(pc)
                except Exception:
                    pass
            # Fully remove the now-empty collection data-block so it does not
            # linger as an empty folder in the Outliner after live preview
            # is switched off (matches ops_split.py behavior).
            try:
                bpy.data.collections.remove(pc)
            except Exception:
                pass
    except Exception:
        pass


# ---------------------------
# BBox and projection
# ---------------------------

def _bb_world(obj):
    """Return the 8 corners of the world-axis-aligned bounding box of an object.

    For plain meshes the box is TIGHT around the real vertices (vertices transformed by
    matrix_world). This equals the box you get after Ctrl+A > Rotation & Scale, but the
    mesh and the object transform stay untouched. The old approach (rotating the local
    bound_box into world space) gives a box that is far too large for rotated round
    shapes such as an icosphere, which breaks seam contact detection.

    Falls back to the rotated local bound_box for non-mesh objects, objects with
    modifiers (the evaluated shape differs from the base mesh), objects in Edit Mode
    (mesh data is not up to date) and on any error.
    """
    try:
        if (obj.type == 'MESH' and obj.mode == 'OBJECT'
                and len(obj.modifiers) == 0
                and obj.data is not None and len(obj.data.vertices) > 0):
            import numpy as np  # local import: no change to the module header needed

            me = obj.data
            n = len(me.vertices)
            co = np.empty(n * 3, dtype=np.float32)
            me.vertices.foreach_get("co", co)
            co = co.reshape(n, 3).astype(np.float64)

            # World transform: p_world = R*S * p_local + t
            m = np.array([list(row) for row in obj.matrix_world], dtype=np.float64)
            world = co @ m[:3, :3].T + m[:3, 3]

            mn = world.min(axis=0)
            mx = world.max(axis=0)

            # Same corner structure as bound_box: 8 corners of the axis-aligned box
            return [Vector((x, y, z))
                    for x in (float(mn[0]), float(mx[0]))
                    for y in (float(mn[1]), float(mx[1]))
                    for z in (float(mn[2]), float(mx[2]))]
    except Exception as ex:
        print(f"[SnapSplit] _bb_world: tight box failed, using bound_box: {ex}")

    # Fallback: previous behaviour (rotated local bounding box)
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]


# ---------------------------
# Slanted seams (contact planes that are not parallel to a world axis)
# ---------------------------

# Custom property keys written by SNAP_OT_align_faces on the moved object
_SEAM_KEY_ORIGIN = "snapsplit_seam_origin"
_SEAM_KEY_NORMAL = "snapsplit_seam_normal"
_SEAM_KEY_XDIR = "snapsplit_seam_xdir"
_SEAM_KEY_PARTNER = "snapsplit_seam_partner"


def _world_verts_np(obj):
    """Return an (N, 3) float64 array of world-space vertex positions, or None.

    Only plain meshes in Object Mode without modifiers are supported; everything else
    returns None so that callers can fall back to the old behaviour.
    """
    try:
        if not (obj.type == 'MESH' and obj.mode == 'OBJECT'
                and len(obj.modifiers) == 0
                and obj.data is not None and len(obj.data.vertices) > 0):
            return None
        import numpy as np  # local import: no change to the module header needed
        me = obj.data
        n = len(me.vertices)
        co = np.empty(n * 3, dtype=np.float32)
        me.vertices.foreach_get("co", co)
        co = co.reshape(n, 3).astype(np.float64)
        m = np.array([list(row) for row in obj.matrix_world], dtype=np.float64)
        return co @ m[:3, :3].T + m[:3, 3]
    except Exception:
        return None


def _orient_normal_to_positive_axis(n):
    """Flip n so that its dominant world-axis component is positive.

    This generalises the axis rule 'socket lies on the +axis side' to slanted seams:
    for an axis-parallel normal the result is identical to the existing behaviour.
    """
    i = max(range(3), key=lambda k: abs(n[k]))
    return n.copy() if n[i] >= 0.0 else -n


def _stored_seam_candidate(obj_p, obj_q):
    """Read the seam data written by Align Faces from either object.

    Returns (origin, normal, xdir) as world-space Vectors, or None if no data exists
    or the stored partner name does not match the other object.
    """
    for holder, other in ((obj_p, obj_q), (obj_q, obj_p)):
        try:
            if holder.get(_SEAM_KEY_PARTNER) != other.name:
                continue
            origin = Vector(holder[_SEAM_KEY_ORIGIN])
            normal = Vector(holder[_SEAM_KEY_NORMAL])
            xdir = Vector(holder[_SEAM_KEY_XDIR])
            if normal.length < 1e-9:
                continue
            return origin, normal.normalized(), xdir
        except Exception:
            continue
    return None


def _resolve_pair_plane(obj_p, obj_q, tol=None):
    """Find a slanted seam between two parts from the stored Align data.

    The stored plane is VALIDATED against the real vertices: one part must lie completely
    behind the plane, the other completely in front of it, and both must touch it.
    If the parts were moved after the alignment the check fails and None is returned.
    Axis-parallel planes return None on purpose (handled by the box based detection).

    Returns (obj_a, obj_b, origin, z, x) or None, with:
      obj_a = socket (on the side z points to), obj_b = pin,
      z = seam normal pointing from the pin part to the socket part,
      x = in-plane tangent (orthogonal to z).
    """
    try:
        import numpy as np
        if tol is None:
            # Same tolerance (in scene units) as _detect_seam_contact
            tol = max(1e-7, SEAM_CONTACT_TOL_MM * unit_mm())

        cand = _stored_seam_candidate(obj_p, obj_q)
        if cand is None:
            return None
        origin, normal, xdir = cand
        z = _orient_normal_to_positive_axis(normal)

        # Axis-parallel seams are handled by the box based detection (unchanged behaviour)
        if max(abs(z.x), abs(z.y), abs(z.z)) > 1.0 - 1e-6:
            return None

        vp = _world_verts_np(obj_p)
        vq = _world_verts_np(obj_q)
        if vp is None or vq is None:
            return None

        o = np.array([origin.x, origin.y, origin.z])
        nz = np.array([z.x, z.y, z.z])
        dp = (vp - o) @ nz
        dq = (vq - o) @ nz

        def behind(d):
            # whole part behind the plane and touching it
            return -tol <= d.max() <= tol

        def in_front(d):
            # whole part in front of the plane and touching it
            return -tol <= d.min() <= tol

        if behind(dp) and in_front(dq):
            obj_b, obj_a = obj_p, obj_q   # p is the pin, q is the socket
        elif behind(dq) and in_front(dp):
            obj_b, obj_a = obj_q, obj_p
        else:
            return None

        # In-plane tangent: remove the normal component of the stored x direction
        x = xdir - z * xdir.dot(z)
        if x.length < 1e-6:
            x = z.orthogonal()
        x.normalize()
        return obj_a, obj_b, origin, z, x
    except Exception as ex:
        print(f"[SnapSplit] _resolve_pair_plane failed: {ex}")
        return None


def _slanted_contact_patch(obj_a, obj_b, origin, z, x, tol=None):
    """Measure the real contact patch of two parts on a slanted seam plane.

    Uses only the vertices that lie within 'tol' of the plane and intersects the extents
    of both parts in the plane's (x, y) frame. For an icosphere touching a cube this is
    the small triangle and not the whole bounding box.

    Returns (center_world, x_axis, y_axis, (u_min, u_max, v_min, v_max)) or None.
    """
    try:
        import numpy as np
        if tol is None:
            tol = max(1e-7, SEAM_CONTACT_TOL_MM * unit_mm())
        y = z.cross(x).normalized()          # x cross y = z (right-handed frame)
        o = np.array([origin.x, origin.y, origin.z])
        nz = np.array([z.x, z.y, z.z])
        ax = np.array([x.x, x.y, x.z])
        ay = np.array([y.x, y.y, y.z])

        spans = []
        for obj in (obj_a, obj_b):
            v = _world_verts_np(obj)
            if v is None:
                return None
            near = v[np.abs((v - o) @ nz) <= tol]
            if len(near) == 0:
                return None
            rel = near - o
            u = rel @ ax
            w = rel @ ay
            spans.append((u.min(), u.max(), w.min(), w.max()))

        u_min = max(spans[0][0], spans[1][0])
        u_max = min(spans[0][1], spans[1][1])
        v_min = max(spans[0][2], spans[1][2])
        v_max = min(spans[0][3], spans[1][3])
        if u_max <= u_min or v_max <= v_min:
            return None  # edge / point contact only

        center = origin + x * float(0.5 * (u_min + u_max)) + y * float(0.5 * (v_min + v_max))
        return center, x, y, (float(u_min), float(u_max), float(v_min), float(v_max))
    except Exception as ex:
        print(f"[SnapSplit] _slanted_contact_patch failed: {ex}")
        return None


# ---------------------------
# Pin / socket role swap
# ---------------------------

def _roles_swapped():
    """True if the user switched the pin/socket definition (scene property swap_pin_socket)."""
    try:
        return bool(bpy.context.scene.snapsplit.swap_pin_socket)
    except Exception:
        return False


def _swap_roles(resolved):
    """Exchange pin and socket in a resolved pair tuple.

    Input:  (a, b, axis, seam_pos, sign[, plane]), a = socket, b = pin.
    Axis seam:    a and b are exchanged and the sign is inverted, so z points the other way.
    Slanted seam: a and b are exchanged and the plane normal z is inverted; the sign is not
                  used there (it stays as it is).
    """
    if resolved is None:
        return None
    a, b, axis, seam_pos, sign = resolved[:5]
    tail = tuple(resolved[5:])
    if tail and tail[0] is not None:
        origin, z, x = tail[0]
        return (b, a, axis, seam_pos, sign, (origin, -z, x)) + tail[1:]
    return (b, a, axis, seam_pos, -sign) + tail


def _maybe_swap(resolved):
    """Apply the role swap only if the scene switch is on."""
    return _swap_roles(resolved) if _roles_swapped() else resolved


def _proj_interval(points, axis_dir, origin):
    """Project points onto a direction (axis_dir) and return min/max distances from origin."""
    a = axis_dir.normalized()
    return (min((p - origin).dot(a) for p in points),
            max((p - origin).dot(a) for p in points))


def _axis_index(axis):
    """Return index 0/1/2 for X/Y/Z axis string."""
    return {"X": 0, "Y": 1, "Z": 2}[axis]


def _axis_vectors(axis):
    """Return normal and two tangential unit vectors for a given axis string."""
    # axis denotes seam normal here (split axis)
    if axis == "X":
        return Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    if axis == "Y":
        return Vector((0, 1, 0)), Vector((1, 0, 0)), Vector((0, 0, 1))
    return Vector((0, 0, 1)), Vector((1, 0, 0)), Vector((0, 1, 0))


# ---------------------------
# Seam detection from geometry (works for cut parts AND for parts joined by Align Faces)
# ---------------------------


# Max. distance (mm) between two bounding-box faces that still counts as "touching".
SEAM_CONTACT_TOL_MM = 0.05


def _axis_unit_vector(axis):
    """Return a fresh world unit vector for the axis letter (fallback: Z)."""
    return {"X": Vector((1, 0, 0)),
            "Y": Vector((0, 1, 0)),
            "Z": Vector((0, 0, 1))}.get(axis, Vector((0, 0, 1)))


def _world_aabb_min_max(obj):
    """Return the world-space AABB as two lists (min[3], max[3]); tight around the vertices, see _bb_world()."""

    corners = _bb_world(obj)
    mn = [min(c[i] for c in corners) for i in range(3)]
    mx = [max(c[i] for c in corners) for i in range(3)]
    return mn, mx


def _detect_seam_contact(obj_p, obj_q):
    """Detect an axis-aligned face contact between the world AABBs of two objects.

    Returns (axis_letter, seam_pos, sign) or None.
    - axis_letter: world axis that is the seam normal (X/Y/Z)
    - seam_pos: world coordinate of the contact plane along that axis
    - sign: +1 if Q lies on the +axis side of P, -1 if on the -axis side
    The axis with the largest contact area wins. Returns None for edge/corner
    contact, gaps, or contact planes that are not parallel to a world axis.
    (The boxes are tight around the real vertices, see _bb_world(), so rotated
    parts such as an icosphere aligned to an axis-parallel face are detected too.)

    """
    tol = max(1e-7, SEAM_CONTACT_TOL_MM * unit_mm())
    p_min, p_max = _world_aabb_min_max(obj_p)
    q_min, q_max = _world_aabb_min_max(obj_q)

    best = None  # (area, axis_letter, seam_pos, sign)
    for i, letter in enumerate(("X", "Y", "Z")):
        o1 = (i + 1) % 3
        o2 = (i + 2) % 3

        # The contact face must have a real overlap on both tangential axes
        ov1 = min(p_max[o1], q_max[o1]) - max(p_min[o1], q_min[o1])
        ov2 = min(p_max[o2], q_max[o2]) - max(p_min[o2], q_min[o2])
        if ov1 <= tol or ov2 <= tol:
            continue

        # Distance between facing box sides along the candidate axis
        gap_up = q_min[i] - p_max[i]   # Q above P
        gap_dn = p_min[i] - q_max[i]   # Q below P
        if abs(gap_up) <= abs(gap_dn):
            gap, sign, seam = gap_up, 1, 0.5 * (q_min[i] + p_max[i])
        else:
            gap, sign, seam = gap_dn, -1, 0.5 * (p_min[i] + q_max[i])
        if abs(gap) > tol:
            continue

        area = ov1 * ov2
        if best is None or area > best[0]:
            best = (area, letter, seam, sign)

    if best is None:
        return None
    return best[1], best[2], best[3]


def _resolve_pair(obj_p, obj_q):
    """Resolve the seam and roles of a part pair; honours the 'Swap Pin / Socket' switch."""
    return _maybe_swap(_resolve_pair_raw(obj_p, obj_q))

def _resolve_freehand_pair_raw(obj_p, obj_q):
    """Adapt a validated Freehand seam to the existing connector pair format."""
    result = resolve_freehand_plane(obj_p, obj_q)

    if result is None:
        return None

    socket, pin, origin, normal, tangent = result
    axis = _world_axis_letter_from_direction(normal)
    position = float(origin[_axis_index(axis)])

    return (
        socket,
        pin,
        axis,
        position,
        1,
        (origin, normal, tangent),
    )


def diagnose_selected_freehand_pair():
    """Validate two selected partners without generating any geometry."""
    objects = list(bpy.context.selected_objects)

    if len(objects) != 2:
        print("[SnapSplit C2] Select exactly two Freehand result objects.")
        return None

    try:
        result = _resolve_freehand_pair_raw(*objects)

        if result is None:
            print("[SnapSplit C2] No shared Freehand seam was found.")
            return None

        result = _maybe_swap(result)
        socket, pin = result[:2]
        origin, normal, tangent = result[5]

        print("[SnapSplit C2] VALID")
        print(f"  Socket: {socket.name}")
        print(f"  Pin: {pin.name}")
        print(f"  Origin: {tuple(origin)}")
        print(f"  Normal: {tuple(normal)}")
        print(f"  Tangent: {tuple(tangent)}")
        print("  Placement uses the existing explicit-plane pipeline.")
        print("  Material-boundary and wall-depth checks are not enabled.")

        return result

    except SeamValidationError as exc:
        print(f"[SnapSplit C2] REJECTED: {exc}")
        return None


def _resolve_pair_raw(obj_p, obj_q):
    """Resolve current contact independently of historical seam ownership."""
    tolerance = max(1e-7, SEAM_CONTACT_TOL_MM * unit_mm())
    return resolve_current_contact(obj_p, obj_q, tolerance)



def _build_connector_pairs(parts, fallback_axis, warn=False):
    """Build detected pairs, preserving explicit Freehand seam planes."""
    objs = [o for o in parts if o is not None]
    pairs = []

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            res = _resolve_pair(objs[i], objs[j])
            if res is not None:
                pairs.append(res)

    if pairs:
        if warn:
            used = {id(o) for pr in pairs for o in pr[:2]}
            if any(id(o) not in used for o in objs):
                report_user(
                    None,
                    'WARNING',
                    'Some selected parts have no valid contact partner '
                    'and were skipped.',
                )
        return pairs


    if warn:
        report_user(
            None,
            'WARNING',
            "No shared planar contact area was found between "
            "the selected parts. No Split Axis fallback was used.",
        )

    return []





def _pair_seam_plane_pos(obj_a, obj_b, axis, props):
    """Return the world-space seam plane coordinate along axis for the pair (A,B).

    Uses the real contact plane if the pair touches along this axis. Otherwise it
    falls back to the middle of the combined bounding box (legacy behaviour,
    without the old split_offset_mm shift).
    """
    contact = _detect_seam_contact(obj_a, obj_b)
    if contact is not None and contact[0] == axis:
        return contact[1]

    idx = _axis_index(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)
    vals_a = [c[idx] for c in bb_a]; vals_b = [c[idx] for c in bb_b]
    lo = min(min(vals_a), min(vals_b))
    hi = max(max(vals_a), max(vals_b))
    if not (lo < hi):
        return lo  # degenerate but safe
    return 0.5 * (lo + hi)



# ---------------------------
# Distribution helpers honoring seam plane
# ---------------------------

def distribute_points_line_on_seam(obj_a, obj_b, count, axis, seam_pos, margin_pct=10.0):
    """Distribute 'count' points along the overlap line of (A,B) on the given seam plane."""
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    ol1 = max(0.0, min(t1_max_a, t1_max_b) - max(t1_min_a, t1_min_b))
    ol2 = max(0.0, min(t2_max_a, t2_max_b) - max(t2_min_a, t2_min_b))

    if ol1 >= ol2:
        t = t1.normalized()
        lo = max(t1_min_a, t1_min_b)
        hi = min(t1_max_a, t1_max_b)
        span = ol1
    else:
        t = t2.normalized()
        lo = max(t2_min_a, t2_min_b)
        hi = min(t2_max_a, t2_max_b)
        span = ol2

    if span <= 0.0:
        return [origin for _ in range(max(1, count))]

    m = max(0.0, float(margin_pct)) * 0.01 * span
    lo_i, hi_i = lo + m, hi - m
    if hi_i < lo_i:
        mid = (lo + hi) * 0.5
        return [origin + t * mid for _ in range(max(1, count))]

    if count <= 1:
        mid = (lo_i + hi_i) * 0.5
        return [origin + t * mid]

    pts = []
    for i in range(count):
        f = i / (count - 1)
        s = lo_i * (1.0 - f) + hi_i * f
        pts.append(origin + t * s)
    return pts


def distribute_points_grid_on_seam(obj_a, obj_b, cols, rows, axis, seam_pos, margin_pct=10.0):
    """Distribute cols*rows points over the 2D overlap of (A,B) on the given seam plane."""
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    def interval_overlap(a_min, a_max, b_min, b_max):
        lo = max(a_min, b_min); hi = min(a_max, b_max)
        return lo, hi, max(0.0, hi - lo)

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    lo1, hi1, span1 = interval_overlap(t1_min_a, t1_max_a, t1_min_b, t1_max_b)
    lo2, hi2, span2 = interval_overlap(t2_min_a, t2_max_a, t2_min_b, t2_max_b)

    if span1 <= 0.0 or span2 <= 0.0:
        return distribute_points_line_on_seam(obj_a, obj_b, cols, axis, seam_pos, margin_pct)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    lo1_i, hi1_i = lo1 + m1, hi1 - m1
    lo2_i, hi2_i = lo2 + m2, hi2 - m2
    if hi1_i < lo1_i or hi2_i < lo2_i:
        c = origin + t1.normalized() * ((lo1 + hi1) * 0.5) + t2.normalized() * ((lo2 + hi2) * 0.5)
        return [c for _ in range(max(1, cols * rows))]

    t1n = t1.normalized(); t2n = t2.normalized()

    pts = []
    for r in range(rows):
        fr = r / (rows - 1) if rows > 1 else 0.5
        sr = lo2_i * (1.0 - fr) + hi2_i * fr
        for c in range(cols):
            fc = c / (cols - 1) if cols > 1 else 0.5
            sc = lo1_i * (1.0 - fc) + hi1_i * fc
            pts.append(origin + t1n * sc + t2n * sr)
    return pts

def distribute_points_on_plane(obj_a, obj_b, plane, distribution, cols, rows, margin_pct=10.0):
    """Distribute connector points on a slanted seam plane.

    plane = (origin, z, x) as returned by _resolve_pair_plane(). The points lie inside the
    real contact patch (vertices near the plane), not inside the bounding boxes.
    distribution is "LINE" (cols points along the longer side) or "GRID" (cols x rows).
    """
    origin, z, x = plane
    patch = _slanted_contact_patch(obj_a, obj_b, origin, z, x)
    if patch is None:
        # No measurable patch: fall back to the stored seam origin
        n_pts = max(1, cols * rows if distribution == "GRID" else cols)
        return [origin.copy() for _ in range(n_pts)]

    _center, ax, ay, (u0, u1, v0, v1) = patch
    m_pct = max(0.0, float(margin_pct)) * 0.01

    def _inner(lo, hi):
        """Shrink [lo, hi] by the margin; collapse to the middle if nothing is left."""
        m = m_pct * (hi - lo)
        lo_i, hi_i = lo + m, hi - m
        if hi_i < lo_i:
            mid = 0.5 * (lo + hi)
            return mid, mid
        return lo_i, hi_i

    def _lerp(lo, hi, i, n):
        return 0.5 * (lo + hi) if n <= 1 else lo + (hi - lo) * (i / (n - 1))

    if distribution == "GRID":
        lu, hu = _inner(u0, u1)
        lv, hv = _inner(v0, v1)
        pts = []
        for r in range(rows):
            for c in range(cols):
                pts.append(origin + ax * _lerp(lu, hu, c, cols) + ay * _lerp(lv, hv, r, rows))
        return pts

    # LINE: along the longer side of the patch, centered on the other side
    if (u1 - u0) >= (v1 - v0):
        lo, hi = _inner(u0, u1)
        mid_v = 0.5 * (v0 + v1)
        return [origin + ax * _lerp(lo, hi, i, cols) + ay * mid_v for i in range(max(1, cols))]
    lo, hi = _inner(v0, v1)
    mid_u = 0.5 * (u0 + u1)
    return [origin + ay * _lerp(lo, hi, i, cols) + ax * mid_u for i in range(max(1, cols))]


# ---------------------------
# Geometry: base connectors
# ---------------------------

def create_cyl_pin(d_mm=5.0, length_mm=10.0, chamfer_mm=0.0, segments=32, name="SnapSplit_Pin"):
    """Create a cylindrical pin mesh object with optional top chamfer."""
    mm = unit_mm()
    d = float(d_mm) * mm
    L = float(length_mm) * mm
    r = max(1e-9, d * 0.5)

    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False,
        segments=max(8, int(segments)),
        radius1=r, radius2=r, depth=L
    )
    # Bottom at z=0, top at z=L
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

    if chamfer_mm and chamfer_mm > 0.0:
        chamfer = float(chamfer_mm) * mm
        top_z = max(v.co.z for v in bm.verts)
        top_verts = [v for v in bm.verts if abs(v.co.z - top_z) < 1e-7]
        scale = max(0.0, (r - chamfer) / r) if r > 1e-12 else 1.0
        for v in top_verts:
            v.co.x *= scale
            v.co.y *= scale
            v.co.z -= chamfer

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_rect_tenon_quader(w_mm=6.0, length_mm=10.0, chamfer_mm=0.0, name="SnapSplit_Tenon"):
    """Create a rectangular tenon (elongated cube) with optional bevel modifier for chamfer."""
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    sx = w; sy = w; sz = L
    S = Matrix(((sx, 0, 0, 0), (0, sy, 0, 0), (0, 0, sz, 0), (0, 0, 0, 1)))
    bmesh.ops.transform(bm, matrix=S, verts=bm.verts)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    if chamfer_mm and chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'NONE'
    return obj

def create_custom_connector_instance(source_obj, width_mm, length_mm, depth_mm,
                                      chamfer_mm=0.0, name="SnapSplit_Custom"):
    """Duplicate source_obj's local mesh shape and rescale it to the target Width (X) /
    Length (Y) / Depth (Z) in mm, following the same authoring convention as the
    built-in Pin/Tenon connectors (local Z = insertion direction).

    The shape is re-centered on X/Y and its lowest local Z point becomes the embed
    base (z=0), regardless of where the source object's own origin sits, so the
    picked object does not need a specially prepared origin.

    Face normals are recalculated to point consistently outward before the mesh
    is finalized. Unlike the built-in Pin/Tenon/Dovetail primitives (which are
    authored with guaranteed outward winding), an arbitrary user mesh may carry
    flipped or mixed normals. Feeding that into the EXACT boolean solver can
    invert a DIFFERENCE cut and remove far more geometry than the intended
    connector-shaped socket -- up to the entire target part on large scales.

    A non-blocking warning is reported if the source mesh contains non-manifold
    edges (open boundaries or edges shared by more than two faces), since boolean
    results on such meshes can remain unreliable even after the normal fix.

    Optional chamfer_mm adds a Bevel modifier (same pattern as create_rect_tenon_quader
    and create_dovetail_box_uvn); caller is responsible for applying it before any
    boolean operation if needed. NOTE: bevel quality on arbitrary user meshes depends
    on the source topology; non-manifold or highly irregular shapes may bevel
    unpredictably. Modifier-apply failures are caught and reported by the caller.
    """
    if source_obj is None or source_obj.type != 'MESH' or source_obj.data is None:
        return None

    mm = unit_mm()
    bm = bmesh.new()
    bm.from_mesh(source_obj.data)
    if len(bm.verts) == 0:
        bm.free()
        return None

    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    ex = max(max_x - min_x, 1e-9)
    ey = max(max_y - min_y, 1e-9)
    ez = max(max_z - min_z, 1e-9)
    cx = 0.5 * (min_x + max_x)
    cy = 0.5 * (min_y + max_y)

    bmesh.ops.translate(bm, vec=Vector((-cx, -cy, -min_z)), verts=bm.verts)

    target_x = max(float(width_mm), 1e-6) * mm
    target_y = max(float(length_mm), 1e-6) * mm
    target_z = max(float(depth_mm), 1e-6) * mm
    S = Matrix.Diagonal((target_x / ex, target_y / ey, target_z / ez, 1.0))
    bmesh.ops.transform(bm, matrix=S, verts=bm.verts)

    # NEW: detect non-manifold topology (open boundary edges, or edges shared by
    # more than two faces) before touching normals. This is a pure diagnostic
    # check on the already-rescaled bmesh, it does not modify geometry, and does
    # not block placement -- it only informs the user that boolean results on
    # this particular source mesh may stay unreliable regardless of the normal
    # fix applied right below.
    non_manifold_found = any(not e.is_manifold for e in bm.edges)
    if non_manifold_found:
        report_user(None, 'WARNING',
                    _trf("Custom connector source mesh '{name}' has non-manifold geometry (open or multi-shared edges); boolean results may be unreliable.", name=source_obj.name))

    # NEW: recalculate face normals to point consistently outward. This is the
    # actual fix for the "target part disappears" bug: an EXACT-solver DIFFERENCE
    # cut interprets inside/outside via face normals, so flipped normals on the
    # cutter can cause it to remove everything outside the connector shape
    # instead of just the connector-shaped socket volume.
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)

    # Optional chamfer, same pattern as create_rect_tenon_quader/create_dovetail_box_uvn
    if chamfer_mm and chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'NONE'

    return obj


def create_uv_sphere(d_mm=2.0, segments=16, rings=8, name="SnapSphere"):
    """Create a UV sphere mesh object with given diameter and segment counts."""
    mm = unit_mm()
    r = max(1e-9, float(d_mm) * 0.5 * mm)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=max(8, int(segments)),
        v_segments=max(6, int(rings)),
        radius=r,
        calc_uvs=False
    )
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_uv_sphere_preview(d_mm=2.0, segments=12, rings=6, name="SnapSpherePreview"):
    """Create a lightweight wireframe UV sphere for viewport previews."""
    mm = unit_mm()
    r = max(1e-9, float(d_mm) * 0.5 * mm)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=max(8, int(segments)),
        v_segments=max(6, int(rings)),
        radius=r,
        calc_uvs=False
    )
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.display_type = 'WIRE'
    obj.hide_select = True
    return obj


# ---------------------------
# Dovetail geometry (u/v/n relative): new
# ---------------------------

def _safe_mm(v, default):
    """Return a safe float millimeter value with fallback."""
    try:
        return float(v) if v is not None else float(default)
    except Exception:
        return float(default)


def create_dovetail_box_uvn(width_u_mm=10.0, length_v_mm=10.0, depth_n_mm=8.0,
                            signed_taper_pct=0.0, chamfer_mm=0.0, name="SnapSplit_DovetailUVN"):
    """Create a dovetail as a tapered rectangular prism in local (u,v,n):

    - Base face at n=0 (wider in u/v), tip at n=depth_n (narrower/wider per signed taper).
    - Signed taper applies only to in-plane axes (u and v) symmetrically.
      positive -> tip narrower; negative -> tip wider.
    - Depth is not tapered (pure extrusion along n).
    - Optional chamfer_mm adds a Bevel modifier (same pattern as create_rect_tenon_quader);
      caller is responsible for applying it before any boolean operation if needed.
    """

    mm = unit_mm()
    wu = max(0.1, _safe_mm(width_u_mm, 10.0)) * mm
    lv = max(0.1, _safe_mm(length_v_mm, 10.0)) * mm
    dn = max(0.1, _safe_mm(depth_n_mm, 8.0)) * mm

    t = max(-90.0, min(90.0, float(signed_taper_pct))) * 0.01
    # Tip scales equally in u and v; clamp to avoid degeneracy
    s_tip = max(0.05, 1.0 - t)

    wb_u = wu; wb_v = lv
    wt_u = max(0.1 * mm, wu * s_tip)
    wt_v = max(0.1 * mm, lv * s_tip)

    bm = bmesh.new()
    # Base (n=0)
    v0 = bm.verts.new((-0.5 * wb_u, -0.5 * wb_v, 0.0))
    v1 = bm.verts.new(( 0.5 * wb_u, -0.5 * wb_v, 0.0))
    v2 = bm.verts.new(( 0.5 * wb_u,  0.5 * wb_v, 0.0))
    v3 = bm.verts.new((-0.5 * wb_u,  0.5 * wb_v, 0.0))
    # Tip (n=depth)
    v4 = bm.verts.new((-0.5 * wt_u, -0.5 * wt_v, dn))
    v5 = bm.verts.new(( 0.5 * wt_u, -0.5 * wt_v, dn))
    v6 = bm.verts.new(( 0.5 * wt_u,  0.5 * wt_v, dn))
    v7 = bm.verts.new((-0.5 * wt_u,  0.5 * wt_v, dn))

    bm.faces.new([v3, v2, v1, v0])  # base
    bm.faces.new([v4, v5, v6, v7])  # tip
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)

    # Optional chamfer via Bevel modifier (consistent with create_rect_tenon_quader
    # and create_cyl_pin). Not applied here; call sites apply it before boolean ops.
    if chamfer_mm and chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'NONE'

    return obj



# ---------------------------
# Geometry
# ---------------------------

def _tip_width_from_angle(base_w_mm: float, angle_per_side_deg: float) -> float:
    """Approximate tip width (mm) from base width and taper angle per side (legacy helper, kept)."""
    try:
        a = max(0.0, float(angle_per_side_deg))
        pct = max(0.0, min(0.9, 2.0 * tan(radians(a)) / 10.0))
    except Exception:
        pct = 0.25
    tip = max(0.1, float(base_w_mm) * (1.0 - pct))
    return tip


def _compute_tip_from_signed_taper(base_w_mm: float, signed_taper_pct: float) -> float:
    """Legacy helper for symmetric square-section dovetail; kept for compatibility paths."""
    t = max(-60.0, min(60.0, float(signed_taper_pct))) * 0.01
    wb = max(0.1, float(base_w_mm))
    wt = wb * (1.0 - t)
    return max(0.1, wt)


def create_dovetail_quader(base_w_mm=6.0, depth_mm=8.0, taper_pct=None, angle_per_side_deg=None, name="SnapSplit_Dovetail"):
    """Legacy square dovetail (width=length), retained for backward compatibility."""
    mm = unit_mm()
    wb = float(base_w_mm) * mm
    L = float(depth_mm) * mm

    if angle_per_side_deg is not None:
        wt_mm = _tip_width_from_angle(base_w_mm, angle_per_side_deg)
        wt = float(wt_mm) * mm
    else:
        t = 0.25 if taper_pct is None else max(0.0, min(95.0, float(taper_pct))) * 0.01
        wt = max(1e-9, wb * (1.0 - t))

    bm = bmesh.new()
    half_wb = wb * 0.5
    half_wt = wt * 0.5
    v0 = bm.verts.new((-half_wb, -half_wb, 0.0))
    v1 = bm.verts.new(( half_wb, -half_wb, 0.0))
    v2 = bm.verts.new(( half_wb,  half_wb, 0.0))
    v3 = bm.verts.new((-half_wb,  half_wb, 0.0))
    v4 = bm.verts.new((-half_wt, -half_wt, L))
    v5 = bm.verts.new(( half_wt, -half_wt, L))
    v6 = bm.verts.new(( half_wt,  half_wt, L))
    v7 = bm.verts.new((-half_wt,  half_wt, L))
    bm.faces.new([v3, v2, v1, v0])
    bm.faces.new([v4, v5, v6, v7])
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_dovetail_quader_signed(base_w_mm=6.0, depth_mm=8.0, signed_taper_pct=0.0, name="SnapSplit_DovetailSigned"):
    """Legacy square-section dovetail with signed taper; retained for compatibility."""
    mm = unit_mm()
    wb = float(base_w_mm) * mm
    L = float(depth_mm) * mm
    wt_mm = _compute_tip_from_signed_taper(base_w_mm, signed_taper_pct)
    wt = float(wt_mm) * mm

    bm = bmesh.new()
    half_wb = wb * 0.5
    half_wt = wt * 0.5
    v0 = bm.verts.new((-half_wb, -half_wb, 0.0))
    v1 = bm.verts.new(( half_wb, -half_wb, 0.0))
    v2 = bm.verts.new(( half_wb,  half_wb, 0.0))
    v3 = bm.verts.new((-half_wb,  half_wb, 0.0))
    v4 = bm.verts.new((-half_wt, -half_wt, L))
    v5 = bm.verts.new(( half_wt, -half_wt, L))
    v6 = bm.verts.new(( half_wt,  half_wt, L))
    v7 = bm.verts.new((-half_wt,  half_wt, L))
    bm.faces.new([v3, v2, v1, v0])
    bm.faces.new([v4, v5, v6, v7])
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


# ---------------------------
# Boolean helpers and transform robustness
# ---------------------------

def _apply_object_scale_if_needed(obj):
    """Bake a non-unit object scale into the mesh to avoid Boolean instabilities.

    Replaces object.transform_apply (scale only): the scale is written into the vertex
    positions with Mesh.transform(), then obj.scale is reset to 1. The operator is kept
    ONLY as a documented fallback for negative (mirroring) scale, where winding and
    normals must match Blender's own behaviour.
    """
    try:
        if obj is None or obj.type != 'MESH' or obj.data is None:
            return
        sx, sy, sz = obj.scale
        if (abs(sx - 1.0) < 1e-6 and abs(sy - 1.0) < 1e-6 and abs(sz - 1.0) < 1e-6):
            return

        # Mirrored scale flips the winding: keep the proven operator for this rare case
        if sx * sy * sz < 0.0:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            # DOCUMENTED FALLBACK: negative scale, see docstring
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            obj.select_set(False)
            return

        # Shared mesh data would change other objects too: give this object its own copy
        if obj.data.users > 1:
            obj.data = obj.data.copy()

        # Bake the scale into the vertices, then reset the object scale
        obj.data.transform(Matrix.Diagonal(Vector((sx, sy, sz, 1.0))))
        obj.scale = (1.0, 1.0, 1.0)
        obj.data.update()
    except Exception:
        pass



def _set_boolean_solver_with_fallback(mod):
    """Try to set solver EXACT, fallback to FAST/FLOAT if unavailable or apply fails upstream."""
    try:
        items = {i.identifier for i in mod.bl_rna.properties['solver'].enum_items}
        if 'EXACT' in items:
            mod.solver = 'EXACT'
        elif 'FAST' in items:
            mod.solver = 'FAST'
        elif 'FLOAT' in items:
            mod.solver = 'FLOAT'
    except Exception:
        try:
            mod.solver = 'EXACT'
        except Exception:
            pass


def boolean_apply(target_obj, mod):
    """Apply a Boolean (or any) modifier on target_obj with validation and error handling."""
    bpy.context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    try:
        # Mesh-data based apply (replaces the modifier_apply operator)
        apply_modifier_data(target_obj, mod)
    except Exception as e:
        report_user(None, 'WARNING',
                    _trf('Modifier apply failed ({name}): {error}', name=mod.name, error=e))

    target_obj.select_set(False)
    try:
        target_obj.data.validate(verbose=False)
        target_obj.data.update()
    except Exception:
        pass


def cut_socket_with_cutter(target_obj, cutter_obj):
    """Apply a DIFFERENCE Boolean using cutter_obj on target_obj to create a socket."""
    _apply_object_scale_if_needed(cutter_obj)
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    _set_boolean_solver_with_fallback(mod)
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)


# ---------------------------
# TEMP helpers: dispose temporary objects
# ---------------------------

def _dispose_object(obj, remove_data=True):
    """Unlink and remove an object; optionally remove and clear its data if orphaned."""
    if not obj:
        return
    try:
        for coll in list(obj.users_collection):
            try:
                coll.objects.unlink(obj)
            except Exception:
                pass
    except Exception:
        pass
    try:
        md = getattr(obj, "data", None)
        if remove_data and md and hasattr(md, "users") and md.users == 1:
            try:
                if md.__class__.__name__ == "Mesh":
                    bpy.data.meshes.remove(md)
                else:
                    bpy.data.batch_remove((md,))
            except Exception:
                pass
            try:
                obj.data = None
            except Exception:
                pass
    except Exception:
        pass
    try:
        bpy.data.objects.remove(obj)
    except Exception:
        pass


def cut_socket_with_cutter_and_dispose(target_obj, cutter_obj):
    """Apply DIFFERENCE Boolean and dispose the cutter object afterwards."""
    _apply_object_scale_if_needed(cutter_obj)
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    _set_boolean_solver_with_fallback(mod)
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)
    _dispose_object(cutter_obj, remove_data=True)


def union_and_dispose(target_obj, union_obj, name="SnapSplit_Union"):
    """Apply UNION Boolean and dispose the helper object afterwards."""
    _apply_object_scale_if_needed(union_obj)
    mod = target_obj.modifiers.new(name, 'BOOLEAN')
    mod.operation = 'UNION'
    _set_boolean_solver_with_fallback(mod)
    mod.object = union_obj
    boolean_apply(target_obj, mod)
    _dispose_object(union_obj, remove_data=True)

def _snapshot_mesh_data(obj):
    """Create a detached copy of obj's mesh data block, to be restored later if
    a risky Boolean operation on obj produces a degenerate result. Returns the
    copied Mesh data block (not yet assigned to any object), or None on failure.
    """
    try:
        return obj.data.copy()
    except Exception:
        return None


def _restore_mesh_data(obj, backup_mesh):
    """Reassign obj.data to a previously captured backup Mesh data block, then
    remove the data block being replaced if it is now orphaned (0 users)."""
    if backup_mesh is None:
        return
    try:
        old_mesh = obj.data
        obj.data = backup_mesh
        if old_mesh and hasattr(old_mesh, "users") and old_mesh.users == 0:
            try:
                bpy.data.meshes.remove(old_mesh)
            except Exception:
                pass
    except Exception:
        pass

def _mesh_bbox_volume(mesh_data):
    """Compute the local-space bounding-box volume of a Mesh data block from
    its raw vertex coordinates. This is only ever used to compare a single
    object's own mesh before and after a Boolean operation (same object, same
    matrix_world in between), so the local-space volume is a sufficient
    relative "how much geometry is still here" signal -- no world-matrix
    transform is required for that comparison. Returns 0.0 for empty meshes
    or on any error.
    """
    try:
        verts = mesh_data.vertices
        if len(verts) == 0:
            return 0.0
        xs = [v.co.x for v in verts]
        ys = [v.co.y for v in verts]
        zs = [v.co.z for v in verts]
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        dz = max(zs) - min(zs)
        return max(dx, 0.0) * max(dy, 0.0) * max(dz, 0.0)
    except Exception:
        return 0.0


# Default threshold for the bounding-box volume drop check in
# _mesh_is_degenerate(): if the target's bounding-box volume after a Custom
# Connector Boolean operation falls below this fraction of its volume before
# the operation, the result is treated as a collapsed/degenerate Boolean and
# rolled back. Kept as a single named constant so the safety margin can be
# tuned in one place if needed.
CUSTOM_CONNECTOR_BOOLEAN_VOLUME_DROP_THRESHOLD = 0.5


def _mesh_is_degenerate(obj, reference_volume=None, volume_drop_threshold=0.5):
    """Return True if obj's mesh currently looks like a collapsed Boolean result.

    Two independent checks are combined:

    1. Zero-polygon check (original behavior): catches a fully empty mesh.
    2. Bounding-box volume drop check (NEW): catches the more common failure
       mode observed with Custom Connector source meshes (e.g. Suzanne at
       certain Insert Depth percentages), where the EXACT solver does not
       fully empty the mesh but instead collapses most of the target's
       volume into a small degenerate remnant while still leaving a handful
       of polygons behind. A plain polygon-count check misses this case,
       which is exactly why the previous version of this function did not
       catch it.

    reference_volume should be the target object's bounding-box volume
    *before* the Boolean operation (see _mesh_bbox_volume()). If the mesh's
    volume after the operation drops below volume_drop_threshold (default:
    50%) of that reference, the result is treated as degenerate too.
    Pass reference_volume=None to disable the volume check and fall back to
    the zero-polygon check only (e.g. when no meaningful "before" state
    exists).
    """
    try:
        if len(obj.data.polygons) == 0:
            return True
    except Exception:
        return True

    if reference_volume is not None and reference_volume > 1e-12:
        current_volume = _mesh_bbox_volume(obj.data)
        if current_volume < (volume_drop_threshold * reference_volume):
            return True

    return False



def union_and_dispose_safe(target_obj, union_obj, name="SnapSplit_Union", warn_label=None):
    """Safe variant of union_and_dispose() for Custom Connector shapes with
    unpredictable topology. Backs up target_obj's mesh before the UNION,
    validates the result against both the zero-polygon check and the
    bounding-box volume drop check, and retries once with the FAST solver if
    the EXACT solver collapsed the result. Restores the original mesh and
    reports a console warning if both solvers fail, instead of silently
    leaving the part empty or shrunk to a degenerate remnant.
    """
    backup = _snapshot_mesh_data(target_obj)
    reference_volume = _mesh_bbox_volume(backup) if backup is not None else None
    restored = False

    _apply_object_scale_if_needed(union_obj)
    mod = target_obj.modifiers.new(name, 'BOOLEAN')
    mod.operation = 'UNION'
    _set_boolean_solver_with_fallback(mod)
    mod.object = union_obj
    boolean_apply(target_obj, mod)

    if _mesh_is_degenerate(target_obj, reference_volume, CUSTOM_CONNECTOR_BOOLEAN_VOLUME_DROP_THRESHOLD) and backup is not None:
        _restore_mesh_data(target_obj, backup)
        restored = True
        retry_backup = _snapshot_mesh_data(target_obj)

        mod2 = target_obj.modifiers.new(name + "_FastRetry", 'BOOLEAN')
        mod2.operation = 'UNION'
        try:
            mod2.solver = 'FAST'
        except Exception:
            pass
        mod2.object = union_obj
        boolean_apply(target_obj, mod2)

        if _mesh_is_degenerate(target_obj, reference_volume, CUSTOM_CONNECTOR_BOOLEAN_VOLUME_DROP_THRESHOLD) and retry_backup is not None:
            _restore_mesh_data(target_obj, retry_backup)
            report_user(None, 'WARNING',
                        "Custom connector UNION produced degenerate/collapsed geometry; part left unmodified. Try a different Insert geometry.")
        else:
            restored = False
            try:
                if retry_backup is not None and retry_backup.users == 0:
                    bpy.data.meshes.remove(retry_backup)
            except Exception:
                pass

    if not restored and backup is not None:
        try:
            if backup.users == 0:
                bpy.data.meshes.remove(backup)
        except Exception:
            pass

    _dispose_object(union_obj, remove_data=True)



def cut_socket_with_cutter_and_dispose_safe(target_obj, cutter_obj, warn_label=None):
    """Safe variant of cut_socket_with_cutter_and_dispose() for Custom
    Connector socket cuts; applies the same backup / validate (zero-polygon +
    bounding-box volume drop) / retry-with-FAST / restore strategy as
    union_and_dispose_safe(), but for the DIFFERENCE operation.
    """
    backup = _snapshot_mesh_data(target_obj)
    reference_volume = _mesh_bbox_volume(backup) if backup is not None else None
    restored = False

    _apply_object_scale_if_needed(cutter_obj)
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    _set_boolean_solver_with_fallback(mod)
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)

    if _mesh_is_degenerate(target_obj, reference_volume, CUSTOM_CONNECTOR_BOOLEAN_VOLUME_DROP_THRESHOLD) and backup is not None:
        _restore_mesh_data(target_obj, backup)
        restored = True
        retry_backup = _snapshot_mesh_data(target_obj)

        mod2 = target_obj.modifiers.new("SnapSplit_Socket_FastRetry", 'BOOLEAN')
        mod2.operation = 'DIFFERENCE'
        try:
            mod2.solver = 'FAST'
        except Exception:
            pass
        mod2.object = cutter_obj
        boolean_apply(target_obj, mod2)

        if _mesh_is_degenerate(target_obj, reference_volume, CUSTOM_CONNECTOR_BOOLEAN_VOLUME_DROP_THRESHOLD) and retry_backup is not None:
            _restore_mesh_data(target_obj, retry_backup)
            report_user(None, 'WARNING',
                        "Custom connector socket cut produced degenerate/collapsed geometry; part left unmodified. Try a different Insert geometry.")
        else:
            restored = False
            try:
                if retry_backup is not None and retry_backup.users == 0:
                    bpy.data.meshes.remove(retry_backup)
            except Exception:
                pass

    if not restored and backup is not None:
        try:
            if backup.users == 0:
                bpy.data.meshes.remove(backup)
        except Exception:
            pass

    _dispose_object(cutter_obj, remove_data=True)


# ---------------------------
# Snap spheres helpers (for cylindrical Pins)
# ---------------------------

def _ring_height_for_visible_half(length_scene, embed_pct):
    """Return the center Z of the protruding half (part B side) along the frame Z-axis."""
    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
    return embed_pct * length_scene + 0.5 * L_free


def _choose_visible_half_robust(base_matrix, zA, zB):
    """Choose which local Z (A or B) protrudes in world coordinates using the frame Z-axis."""
    try:
        z_axis_world = Vector((base_matrix[0][2], base_matrix[1][2], base_matrix[2][2])).normalized()
        p0_w = Vector((base_matrix[0][3], base_matrix[1][3], base_matrix[2][3]))
        pA_w = base_matrix @ Vector((0.0, 0.0, zA, 1.0))
        pB_w = base_matrix @ Vector((0.0, 0.0, zB, 1.0))
        dA = (Vector((pA_w.x, pA_w.y, pA_w.z)) - p0_w).dot(z_axis_world)
        dB = (Vector((pB_w.x, pB_w.y, pB_w.z)) - p0_w).dot(z_axis_world)
        return zB if dB >= dA else zA
    except Exception:
        return zB


def add_snap_spheres_for_cyl_pin(base_matrix, pin_radius_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
    """Add a ring of snap spheres around a cylindrical pin; union to B, socket to A, and dispose helpers."""
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * length_scene
    zB = _ring_height_for_visible_half(length_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)

    import math
    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = pin_radius_scene + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * math.pi) * (i / n_per_side)
        nx = math.cos(ang); ny = math.sin(ang)

        local_pos = Vector((r_center * nx, r_center * ny, ring_z))
        world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
        world_pos = Vector((world_pos.x, world_pos.y, world_pos.z))

        sphere = create_uv_sphere(d_mm=d_sph_mm, segments=24, rings=12, name=f"{name_prefix}_Snap_{i}")
        M = Matrix.Translation(world_pos)
        sphere.matrix_world = M
        cutters_coll.objects.link(sphere)

        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)

        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))

        union_and_dispose(part_b, sphere, name=f"{name_prefix}_SnapU_{i}")
        cut_socket_with_cutter_and_dispose(part_a, sph_cut)

        created.append(None)
    return created


# ---------------------------
# Sphere-placement helpers (for rectangular Tenon-as-Quader; ring like pin)
# ---------------------------

def add_snap_spheres_for_rect_tenon_ring(base_matrix, half_w_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
    """Add a ring of snap spheres around a square-section tenon; union to B, socket to A, and dispose helpers."""
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * length_scene
    zB = _ring_height_for_visible_half(length_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)

    import math
    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = half_w_scene + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * math.pi) * (i / n_per_side)
        nx = math.cos(ang); ny = math.sin(ang)

        local_pos = Vector((r_center * nx, r_center * ny, ring_z))
        world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
        world_pos = Vector((world_pos.x, world_pos.y, world_pos.z))

        sphere = create_uv_sphere(d_mm=d_sph_mm, segments=24, rings=12, name=f"{name_prefix}_Snap_{i}")
        M = Matrix.Translation(world_pos)
        sphere.matrix_world = M
        cutters_coll.objects.link(sphere)

        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)

        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))

        union_and_dispose(part_b, sphere, name=f"{name_prefix}_SnapU_{i}")
        cut_socket_with_cutter_and_dispose(part_a, sph_cut)

        created.append(None)
    return created

# ---------------------------
# Sphere-ring helper for tapered Dovetail cross-section.
# ---------------------------

def add_snap_spheres_for_dovetail_ring(base_matrix, width_u_mm, length_v_mm,
                                        depth_n_mm, signed_taper_pct, props,
                                        name_prefix, part_a, part_b, cutters_coll):
    """Add a ring of snap spheres around a tapered dovetail wedge.

    Unlike the constant-radius pin/tenon rings, the dovetail's u/v half-width
    changes linearly along n (see create_dovetail_box_uvn). The ring radius is
    therefore computed from the half-width at the ring height, interpolated
    with the exact same formula used to build the wedge geometry, so the
    spheres sit precisely on the real (possibly tapered or widened) side wall
    instead of on the unverjuengt base width. Reference axis is u (Width),
    analogous to half_w_scene in add_snap_spheres_for_rect_tenon_ring.
    Union to B, socket to A, and dispose helpers — same pattern as the other
    ring helpers (add_snap_spheres_for_cyl_pin / _for_rect_tenon_ring).
    """
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    # depth_n acts as the "length" axis here (embed/protrusion direction n),
    # guarded against zero/negative input to avoid a division by zero below.
    depth_n_scene = max(0.1 * mm, float(depth_n_mm) * mm)
    width_u_scene = max(0.1 * mm, float(width_u_mm) * mm)

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * depth_n_scene
    zB = _ring_height_for_visible_half(depth_n_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)
    # Safety clamp: _choose_visible_half_robust should already return zA or zB,
    # but clamp defensively so the interpolation fraction below stays in [0, 1]
    # even in edge cases (e.g. unusual embed percentages).
    ring_z = max(0.0, min(depth_n_scene, ring_z))

    # Interpolate the half-width at ring_z using the SAME taper formula as
    # create_dovetail_box_uvn(): t = clamp(taper, -90, 90) * 0.01,
    # s_tip = max(0.05, 1 - t), then linear lerp between base and tip half-width.
    t = max(-90.0, min(90.0, float(signed_taper_pct))) * 0.01
    s_tip = max(0.05, 1.0 - t)
    half_wb_u = 0.5 * width_u_scene
    half_wt_u = max(0.05 * mm, half_wb_u * s_tip)
    frac = ring_z / depth_n_scene
    half_u_at_ring = half_wb_u + (half_wt_u - half_wb_u) * frac

    import math
    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = half_u_at_ring + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * math.pi) * (i / n_per_side)
        nx = math.cos(ang); ny = math.sin(ang)

        local_pos = Vector((r_center * nx, r_center * ny, ring_z))
        world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
        world_pos = Vector((world_pos.x, world_pos.y, world_pos.z))

        sphere = create_uv_sphere(d_mm=d_sph_mm, segments=24, rings=12, name=f"{name_prefix}_Snap_{i}")
        M = Matrix.Translation(world_pos)
        sphere.matrix_world = M
        cutters_coll.objects.link(sphere)

        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)

        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))

        union_and_dispose(part_b, sphere, name=f"{name_prefix}_SnapU_{i}")
        cut_socket_with_cutter_and_dispose(part_a, sph_cut)

        created.append(None)
    return created


# ---------------------------
# Dovetail helpers: span width, frame ops, side-cut
# ---------------------------

# Optional in-plane tangent hint for slanted seams. It is only set while the click operator
# places a connector (the place_one_*_at() helpers build their own frame); None means
# "derive x from world X" (previous behaviour).
_FRAME_X_HINT = None


def _set_frame_x_hint(x_dir):
    """Set (Vector) or clear (None) the module-wide in-plane tangent hint."""
    global _FRAME_X_HINT
    _FRAME_X_HINT = x_dir.copy() if x_dir is not None else None


def _orthonormal_frame_from_z(z: Vector, x_hint=None):
    """Build a stable orthonormal frame (x,y,z) from a given z-axis.

    If x_hint (or the module-wide hint) is given, x is the hint projected into the plane
    orthogonal to z. Otherwise x is derived from the world X axis (previous behaviour).
    """
    z = z.normalized()
    if x_hint is None:
        x_hint = _FRAME_X_HINT
    if x_hint is not None:
        xh = x_hint - z * x_hint.dot(z)
        if xh.length > 1e-6:
            x = xh.normalized()
            y = z.cross(x); y.normalize()   # x cross y = z (right-handed)
            return x, y, z
    x = Vector((1, 0, 0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0, 1, 0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()
    return x, y, z



def _apply_inplane_offset_and_rotation(M: Matrix, offset_u_mm: float, offset_v_mm: float, rotation_deg: float):
    """Apply an in-plane translation along local X/Y (u = width, v = length seam axes)
    and a rotation around local Z. Translation happens in the unrotated local frame,
    so the u/v offsets stay tied to the fixed seam-plane axes regardless of rotation."""
    mm = unit_mm()
    off_u = float(offset_u_mm) * mm
    off_v = float(offset_v_mm) * mm
    ang = radians(float(rotation_deg))
    # Local transforms: T_uv(off_u, off_v) then R_z(ang)
    T = Matrix.Translation((off_u, off_v, 0.0))
    R = Matrix.Rotation(ang, 4, 'Z')
    return M @ T @ R



def _compute_edge_to_edge_span_width(a, b, axis, seam_pos, margin_pct=5.0):
    """Return the span length along the longer in-plane overlap axis on the seam plane (scene units)."""
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(a); bb_b = _bb_world(b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    ol1 = max(0.0, min(t1_max_a, t1_max_b) - max(t1_min_a, t1_min_b))
    ol2 = max(0.0, min(t2_max_a, t2_max_b) - max(t2_min_a, t2_min_b))
    span = max(ol1, ol2)

    m = max(0.0, float(margin_pct)) * 0.01 * span
    effective = max(0.0, span - 2.0 * m)
    return effective


def _compute_edge_to_edge_span_along_dir(a, b, measure_dir: Vector, axis: str, seam_pos, margin_pct=5.0):
    """Return the span length along a chosen in-plane direction on the seam plane (scene units)."""
    n_axis, t1, t2 = _axis_vectors(axis)
    dirn = measure_dir.normalized()
    bb_a = _bb_world(a); bb_b = _bb_world(b)
    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    min_a, max_a = _proj_interval(bb_a, dirn, origin)
    min_b, max_b = _proj_interval(bb_b, dirn, origin)
    lo = max(min_a, min_b)
    hi = min(max_a, max_b)
    span = max(0.0, hi - lo)

    m = max(0.0, float(margin_pct)) * 0.01 * span
    effective = max(0.0, span - 2.0 * m)
    return effective


# ---------------------------
# NEW: fixed internal safety overshoot for the Dovetail SOCKET cutter only.
#
# Problem observed: when the socket cutter's in-plane (u/v) side faces land
# exactly on / very close to the target's own outer surface (e.g. AUTO span
# with margin, or a manually entered size that matches the stock exactly),
# Blender's EXACT Boolean solver can leave a thin, un-cut strip of the outer
# hull standing ("skin remains closed") instead of producing a clean cut all
# the way through to the edge. Coincident/near-coincident faces are a known
# weak spot of the EXACT solver.
#
# Fix: always enlarge ONLY the socket (DIFFERENCE) cutter's u/v dimensions by
# a small fixed amount on each side. This guarantees genuine volume overlap
# with the target's outer wall instead of a coplanar touch, without changing
# the visible tenon geometry that gets unioned into part B.
# ---------------------------------------------------------------------------

# Fixed internal safety margin (mm), applied per side (so total growth in a
# given in-plane dimension is 2 * this value). Kept small so it stays well
# below typical tolerance/print accuracy and does not visibly change the fit.
_DOVETAIL_SOCKET_SIDE_OVERSHOOT_MM = 0.5


def _uvn_socket_size_with_overshoot(width_u_mm, length_v_mm, overshoot_mm=_DOVETAIL_SOCKET_SIDE_OVERSHOOT_MM):
    """Return (width_u_mm, length_v_mm) enlarged symmetrically by a fixed overshoot per side.

    This is used exclusively for the Dovetail socket (DIFFERENCE) cutter so its
    side faces always cut slightly past the target's outer surface instead of
    landing exactly on it (or just short of it after AUTO-span margin), which
    avoids leftover "skin" from coplanar/near-coplanar Boolean faces. The
    visible tenon geometry (UNION into part B) is intentionally NOT affected.
    """
    ow = max(0.0, float(overshoot_mm))
    return (max(0.1, float(width_u_mm) + 2.0 * ow),
            max(0.1, float(length_v_mm) + 2.0 * ow))


def _combined_world_bounds(objects):
    """Return combined world AABB (min, max) as 3D vectors for a list of objects.

    NOTE: kept as a small generic utility. It is no longer used by the dovetail
    hard-side-cut path (see _build_combined_solid_for_clip / _clip_helper_to_combined_surface
    below), because an axis-aligned box cannot correctly trim connectors against
    curved/organic outer surfaces.
    """
    if not objects:
        z = Vector((0, 0, 0))
        return z.copy(), z.copy()
    mins = Vector((float('inf'), float('inf'), float('inf')))
    maxs = Vector((-float('inf'), -float('inf'), -float('inf')))
    for o in objects:
        for c in _bb_world(o):
            mins.x = min(mins.x, c.x)
            mins.y = min(mins.y, c.y)
            mins.z = min(mins.z, c.z)
            maxs.x = max(maxs.x, c.x)
            maxs.y = max(maxs.y, c.y)
            maxs.z = max(maxs.z, c.z)
    return mins, maxs


# NEW: -------------------------------------------------------------
# Hard-side cut v2: real surface clipping instead of axis-aligned slabs.
#
# The previous implementation trimmed overhanging dovetail geometry with two
# thin (1 Blender-unit) axis-aligned slab cutters. This failed whenever the
# overhang exceeded that thickness, or when the outer hull was curved/organic
# (an AABB face can never follow a curved surface). The new approach clips the
# connector geometry directly against the real combined solid of both split
# parts (A union B), which reconstructs the object's true outer hull.
# ---------------------------------------------------------------------------

def _recalc_normals_outside(obj):
    """Recalculate face normals to point outward (improves Boolean solver stability).

    Pure BMesh version. Replaces the former Edit Mode sequence
    mode_set(EDIT) + mesh.select_all(SELECT) + mesh.normals_make_consistent(inside=False).
    Works in Object Mode (temporary BMesh, written back) and directly on the edit
    BMesh if the object happens to be in Edit Mode.
    NOTE: unlike the old version this does not change the selection or the active object.
    """
    if not obj or obj.type != 'MESH' or obj.data is None:
        return
    try:
        if obj.mode == 'EDIT':
            # Live edit BMesh: modify in place and flush to the viewport
            bm = bmesh.from_edit_mesh(obj.data)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bmesh.update_edit_mesh(obj.data)
        else:
            # Object Mode: read into a temporary BMesh and write back
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
                bm.to_mesh(obj.data)
            finally:
                bm.free()
            obj.data.update()
    except Exception as ex:
        print(f"[SnapSplit DEBUG] _recalc_normals_outside failed on "
              f"'{getattr(obj, 'name', '?')}': {ex}")



def _build_combined_solid_for_clip(a, b, cutters_coll, name="SnapSplit_ClipSolid"):
    """Build a temporary watertight solid representing the true outer hull (A union B).

    This solid is later used as an INTERSECT target so that overhanging dovetail
    geometry gets clipped exactly along the real object surface, including curved
    or fully organic shapes. Returns the linked helper object on success, or None
    if the union failed or produced an empty/degenerate mesh (e.g. seams not closed).
    The caller is responsible for disposing the returned object via _dispose_object.
    """
    clip_obj = None
    b_dup = None
    try:
        # Duplicate A as the base of the clip solid (independent mesh data)
        clip_obj = a.copy()
        clip_obj.data = a.data.copy()
        clip_obj.name = name
        for mod in list(clip_obj.modifiers):
            clip_obj.modifiers.remove(mod)
        cutters_coll.objects.link(clip_obj)

        # Duplicate B to union into the clip solid without touching the real part B
        b_dup = b.copy()
        b_dup.data = b.data.copy()
        b_dup.name = f"{name}_BPart"
        for mod in list(b_dup.modifiers):
            b_dup.modifiers.remove(mod)
        cutters_coll.objects.link(b_dup)

        _apply_object_scale_if_needed(clip_obj)
        _apply_object_scale_if_needed(b_dup)

        mod = clip_obj.modifiers.new("SnapSplit_ClipUnion", 'BOOLEAN')
        mod.operation = 'UNION'
        _set_boolean_solver_with_fallback(mod)
        mod.object = b_dup
        boolean_apply(clip_obj, mod)
        _dispose_object(b_dup, remove_data=True)
        b_dup = None

        # Consistent outward normals reduce EXACT-solver artifacts on the next Boolean
        _recalc_normals_outside(clip_obj)

        if not clip_obj.data or len(clip_obj.data.polygons) == 0:
            _dispose_object(clip_obj, remove_data=True)
            return None

        return clip_obj
    except Exception:
        try:
            if b_dup is not None:
                _dispose_object(b_dup, remove_data=True)
        except Exception:
            pass
        try:
            if clip_obj is not None:
                _dispose_object(clip_obj, remove_data=True)
        except Exception:
            pass
        return None


def _clip_helper_to_combined_surface(helper_obj, clip_solid):
    """Trim helper_obj (dovetail tenon or socket cutter) to the volume inside clip_solid.

    Uses a real Boolean INTERSECT against the true combined outer surface (A union B),
    so the cut follows curved/organic contours exactly instead of an axis-aligned box,
    and there is no fixed cutting depth like the old 1-unit slabs.
    Returns True on success (non-empty result). On failure the modifier attempt has
    already run via boolean_apply(); the caller should warn the user and may keep the
    untrimmed helper_obj rather than silently losing geometry.
    """
    if clip_solid is None or clip_solid.data is None:
        return False
    try:
        mod = helper_obj.modifiers.new("SnapSplit_DVT_SurfaceClip", 'BOOLEAN')
        mod.operation = 'INTERSECT'
        _set_boolean_solver_with_fallback(mod)
        mod.object = clip_solid
        boolean_apply(helper_obj, mod)
        try:
            helper_obj.data.validate(verbose=False)
        except Exception:
            pass
        return helper_obj.data is not None and len(helper_obj.data.polygons) > 0
    except Exception:
        return False


# ---------------------------
# Dovetail helpers: span width, frame ops, side-cut
# ---------------------------

def place_one_cyl_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Pin_Click"):
    """Place one cylindrical pin at a world point; union into B and cut socket into A."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    L_scene = float(props.pin_length_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    seg = int(getattr(props, "pin_segments", 32))
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                         segments=seg, name=f"{name_prefix}")
    pin.matrix_world = M
    cutters_coll.objects.link(pin)
    union_and_dispose(b, pin, name=f"{name_prefix}_Union")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    socket_d = float(props.pin_diameter_mm) + 2.0 * tol
    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None


def place_one_rect_tenon_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Tenon_Click"):
    """Place one rectangular tenon at a world point; union into B and cut socket into A."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    L_scene = float(props.tenon_depth_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm, name=f"{name_prefix}")
    tenon.matrix_world = M
    cutters_coll.objects.link(tenon)
    for mod in list(tenon.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tenon
            tenon.select_set(True)
            try:
                apply_modifier_data(tenon, mod)  # replaces the modifier_apply operator

            except Exception as e:
                report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
            tenon.select_set(False)
    union_and_dispose(b, tenon, name=f"{name_prefix}_Union")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = sx
    sz = 1.0

    socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None

def place_one_custom_connector_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Custom_Click"):
    """Place one Custom Connector (arbitrary source mesh, rescaled) at a world point;
    union into B and cut a tolerant socket into A. Mirrors place_one_dovetail_at()'s
    Span Axis / Hard-side Cut / Chamfer / Placement / Snap Spheres pipeline, reusing
    the exact same shared properties so behavior stays consistent across connector types.
    """
    if props is None:
        props = bpy.context.scene.snapsplit

    source_obj = getattr(props, "custom_connector_object", None)
    if source_obj is None or source_obj.type != 'MESH' or source_obj.data is None:
        report_user(None, 'ERROR', 'Please select a connector object for Custom Connector.')
        return None, None

    warn_if_unapplied_transforms(source_obj)

    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)  # x -> u (Width), y -> v (Length)

    width_mm = float(getattr(props, "custom_connector_width_mm", 6.0))
    length_mm = float(getattr(props, "custom_connector_length_mm", 6.0))
    depth_mm = float(getattr(props, "custom_connector_depth_mm", 8.0))

    # NEW: Span Axis resolution — reuses the shared dovetail_span_axis property so a
    # world axis (X/Y/Z) that lies in the seam plane forces the Custom Connector to
    # overshoot both outer sides along that axis, exactly like the Dovetail pipeline.
    span_axis_choice = str(getattr(props, "dovetail_span_axis", "NONE"))
    span_role = _dovetail_span_axis_role(span_axis_choice, x, y)
    force_hard_cut = False
    if span_role == "U":
        axis_letter = span_axis_choice if span_axis_choice in {"X", "Y", "Z"} else _world_axis_letter_from_direction(x)
        width_mm = _dovetail_forced_span_size_mm(a, b, axis_letter)
        force_hard_cut = True
    elif span_role == "V":
        axis_letter = span_axis_choice if span_axis_choice in {"X", "Y", "Z"} else _world_axis_letter_from_direction(y)
        length_mm = _dovetail_forced_span_size_mm(a, b, axis_letter)
        force_hard_cut = True
    elif span_axis_choice != "NONE" and span_role is None:
        report_user(None, 'WARNING',
                    'Selected Span Axis matches the seam normal, not the seam plane; span axis ignored.')

    L_scene = depth_mm * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    # NEW: In-plane placement — reuses the shared dovetail_inplane_* properties.
    M = _apply_inplane_offset_and_rotation(
        M,
        offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
        offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
        rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
    )

    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # NEW: Hard-side cut — reuses the shared dovetail_hard_side_cut flag, or is forced
    # whenever a Span Axis override was applied above (oversized geometry must be
    # trimmed back to the real outer surface).
    hard_cut_enabled = bool(getattr(props, "dovetail_hard_side_cut", False)) or force_hard_cut
    clip_solid = None
    if hard_cut_enabled:
        clip_solid = _build_combined_solid_for_clip(a, b, cutters_coll)
        if clip_solid is None:
            report_user(None, 'WARNING',
                        'Hard-side cut: could not build combined surface (seam may not be closed); connector left untrimmed.')

    conn = create_custom_connector_instance(source_obj, width_mm, length_mm, depth_mm,
                                             chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                                             name=f"{name_prefix}")
    if conn is None:
        report_user(None, 'ERROR', 'Selected connector object has no usable mesh data.')
        return None, None
    conn.matrix_world = M
    cutters_coll.objects.link(conn)

    # NEW: apply the chamfer bevel modifier before any boolean step, same pattern
    # as place_one_dovetail_at() / the RECT_TENON path.
    for mod in list(conn.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = conn
            conn.select_set(True)
            try:
                apply_modifier_data(conn, mod)  # replaces the modifier_apply operator

            except Exception as e:
                report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
            conn.select_set(False)

    # NEW: clip against the real combined A/B surface instead of leaving overshoot geometry.
    if clip_solid is not None:
        ok = _clip_helper_to_combined_surface(conn, clip_solid)
        if not ok:
            report_user(None, 'WARNING',
                        'Hard-side cut failed on the connector; keeping untrimmed connector geometry.')

    union_and_dispose_safe(b, conn, name=f"{name_prefix}_Union", warn_label=name_prefix)

    mm = unit_mm()
    tol = float(props.effective_tolerance())

    # NEW: fixed safety overshoot on the socket cutter's own u/v size, same helper
    # already used by the Dovetail socket, so the cutter genuinely overlaps A's
    # outer wall instead of landing exactly on it.
    socket_width_mm, socket_length_mm = _uvn_socket_size_with_overshoot(width_mm, length_mm)

    half_w = max(0.5 * socket_width_mm * mm, 1e-9)
    half_l = max(0.5 * socket_length_mm * mm, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = 1.0 + (tol * mm) / half_l
    sz = 1.0

    socket = create_custom_connector_instance(source_obj, socket_width_mm, socket_length_mm, depth_mm,
                                               chamfer_mm=0.0,  # socket cutter stays sharp-edged
                                               name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)
    # NOTE: socket cutter intentionally NOT clipped against clip_solid — same
    # rationale as the Dovetail socket (DIFFERENCE only removes real overlap).
    cut_socket_with_cutter_and_dispose_safe(a, socket, warn_label=name_prefix)

    if clip_solid is not None:
        _dispose_object(clip_solid, remove_data=True)

    # NEW: optional Snap Spheres ring — reuses add_snap_spheres_for_rect_tenon_ring()
    # verbatim, with Custom Width as the reference axis (analogous to how the
    # Dovetail ring uses its Width/u axis, per add_snap_spheres_for_dovetail_ring's
    # own docstring: "Reference axis is u (Width), analogous to half_w_scene in
    # add_snap_spheres_for_rect_tenon_ring").
    if bool(getattr(props, "custom_snap_spheres_enabled", False)):
        half_w_scene = max(0.5 * width_mm * mm, 1e-9)
        add_snap_spheres_for_rect_tenon_ring(
            base_matrix=M,
            half_w_scene=half_w_scene,
            length_scene=depth_mm * mm,
            props=props,
            name_prefix=name_prefix,
            part_a=a,
            part_b=b,
            cutters_coll=cutters_coll
        )

    return None, None

# ---------------------------
# NEW: forced Span Axis support for the Dovetail connector.
#
# Because _orthonormal_frame_from_z() always derives the in-plane u/v basis
# from the seam normal (split axis) using world-aligned fallbacks, u and v are
# always exactly one of the two remaining world axes (up to sign) for X/Y/Z
# seam normals. This lets us resolve a user-forced world axis (X/Y/Z) to
# either the "U" (width) or "V" (length) in-plane role with a simple dot
# product, without needing to know the split axis explicitly.
# ---------------------------------------------------------------------------

def _dovetail_span_axis_role(span_axis_choice: str, x_dir: Vector, y_dir: Vector):
    """Resolve a user-forced Span Axis choice ("NONE"/"AUTO"/"X"/"Y"/"Z") to the
    dovetail's local in-plane role.

    Returns "U" if the chosen world axis matches the local u (x_dir) direction,
    "V" if it matches local v (y_dir), "V" unconditionally for "AUTO" (always
    targets the Dovetail Length axis regardless of world alignment), or None
    if NONE was chosen or the axis coincides with the seam normal itself
    (not in the seam plane).
    """
    if span_axis_choice in (None, "NONE"):
        return None
    if span_axis_choice == "AUTO":
        # Auto always stretches along the local V (Dovetail Length) axis,
        # independent of which world axis it happens to correspond to.
        return "V"
    world_axis = {

        "X": Vector((1.0, 0.0, 0.0)),
        "Y": Vector((0.0, 1.0, 0.0)),
        "Z": Vector((0.0, 0.0, 1.0)),
    }.get(span_axis_choice)
    if world_axis is None:
        return None
    if abs(world_axis.dot(x_dir.normalized())) > 0.99:
        return "U"
    if abs(world_axis.dot(y_dir.normalized())) > 0.99:
        return "V"
    return None


def _world_axis_letter_from_direction(direction: Vector) -> str:
    """Return the world axis letter ("X"/"Y"/"Z") whose basis vector is most
    aligned with the given direction. Used to resolve the "AUTO" Span Axis
    (which always targets the local V/length role) to a concrete world axis
    for extent measurement in _dovetail_forced_span_size_mm(); u/v are always
    exactly world-axis-aligned for X/Y/Z seam normals, so this is exact in
    practice, not just an approximation."""
    d = direction.normalized()
    ax, ay, az = abs(d.x), abs(d.y), abs(d.z)
    if ax >= ay and ax >= az:
        return "X"
    if ay >= ax and ay >= az:
        return "Y"
    return "Z"


def _dovetail_forced_span_size_mm(a, b, axis_letter: str, safety_margin_mm: float = 10.0):

    """Return an in-plane size (mm) along axis_letter (X/Y/Z world axis) that is
    guaranteed to exceed the combined outer extent of A and B along that axis,
    regardless of where the dovetail sits within the seam overlap.

    Uses 2x the combined AABB extent plus a fixed safety margin per side, so
    even a connector placed near one edge of the object still overshoots both
    outer sides. The oversized geometry relies on the hard-side clip (against
    the real A/B surface) to be trimmed back to the true outer contour.
    """
    mins, maxs = _combined_world_bounds([a, b])
    idx = _axis_index(axis_letter)
    extent_scene = maxs[idx] - mins[idx]
    extent_mm = extent_scene / unit_mm()
    return max(0.1, 2.0 * extent_mm + 2.0 * float(safety_margin_mm))


def place_one_dovetail_at(a, b, axis, point_world, frame_z=None, props=None,
name_prefix="Dovetail_Click", return_placement=False):

    """Place one dovetail wedge at a world point; union into B and cut socket into A.

    Updated behavior (only for Dovetail):
    - Axis-relative sizing tied to seam plane (u, v, n):
      Width -> along u, Length -> along v, Depth -> along n.
    - Signed Taper applies in-plane (u/v) only; Depth is not tapered.
    - AUTO span per in-plane axis (optional): width_u/length_v can be derived from overlap extents.
    - Preview == final: same transforms including in-plane offset/rotation.
    - Hard-side Cut clips against the real combined A/B surface (Boolean INTERSECT)
      instead of axis-aligned slab cutters, so overhang is removed reliably even
      on curved/organic outer hulls and regardless of how far the dovetail sticks out.
    - NEW: the socket (DIFFERENCE) cutter's in-plane size always gets a small fixed
      safety overshoot (_DOVETAIL_SOCKET_SIDE_OVERSHOOT_MM) so its side faces cut
      slightly past the target's outer surface instead of landing exactly on it.
      This fixes cases where a thin strip of the outer hull remained uncut (e.g.
      AUTO span, or manual dimensions matching the stock size exactly). Only the
      socket cutter is affected; the visible tenon unioned into part B is unchanged.
    """
    if props is None:
        props = bpy.context.scene.snapsplit

    # Build local UVN from seam normal
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)  # x->u, y->v, z->n

    # Seam plane world coordinate
    try:
        seam_pos = _pair_seam_plane_pos(a, b, axis, props)
    except Exception:
        seam_pos = 0.0

    # Resolve in-plane auto span if requested; otherwise use manual values
    auto_span = bool(getattr(props, "dovetail_auto_span", False))
    margin_pct = float(getattr(props, "dovetail_span_margin_pct", 10.0))

    width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
    length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))  # fallback to width if length not defined
    depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))

    if auto_span:
        # Measure span along u and v separately on the seam plane
        span_u = _compute_edge_to_edge_span_along_dir(a, b, x, axis, seam_pos, margin_pct=margin_pct)
        span_v = _compute_edge_to_edge_span_along_dir(a, b, y, axis, seam_pos, margin_pct=margin_pct)
        width_u_mm = max(span_u / unit_mm(), 0.1)
        length_v_mm = max(span_v / unit_mm(), 0.1)

    # Forced Span Axis: if the user picked a world axis (X/Y/Z) that lies in the
    # seam plane (matches local u or v), override that axis's size so the
    # dovetail is guaranteed to overshoot both outer sides along it. The other
    # in-plane axis is left untouched (manual size or AUTO span result).
    span_axis_choice = str(getattr(props, "dovetail_span_axis", "NONE"))
    span_role = _dovetail_span_axis_role(span_axis_choice, x, y)
    force_hard_cut = False
    if span_role == "U":
        # For X/Y/Z the choice string is already the correct world axis letter;
        # AUTO never resolves to "U" (see _dovetail_span_axis_role).
        axis_letter = span_axis_choice if span_axis_choice in {"X", "Y", "Z"} else _world_axis_letter_from_direction(x)
        width_u_mm = _dovetail_forced_span_size_mm(a, b, axis_letter)
        force_hard_cut = True
    elif span_role == "V":
        # AUTO resolves to "V" but is not itself a valid axis letter for
        # _dovetail_forced_span_size_mm(); resolve the actual world axis
        # that the local v (length) direction corresponds to.
        axis_letter = span_axis_choice if span_axis_choice in {"X", "Y", "Z"} else _world_axis_letter_from_direction(y)
        length_v_mm = _dovetail_forced_span_size_mm(a, b, axis_letter)
        force_hard_cut = True
    elif span_axis_choice != "NONE" and span_role is None:
        report_user(None, 'WARNING',
                    'Selected Span Axis matches the seam normal, not the seam plane; span axis ignored.')


    # Build placement frame at click with embed percentage along n
    L_scene = float(depth_n_mm) * unit_mm()

    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))



    # Apply in-plane controls (offsets along u/width and v/length, rotation around n)
    M = _apply_inplane_offset_and_rotation(
        M,
        offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
        offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
        rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
    )


    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # NEW: Build the real combined-surface clip solid once (A union B), before A/B
    # are modified by this connector's own union/difference operations below.
    # A forced Span Axis always requires the hard-side clip, since the
    # oversized in-plane geometry must be trimmed back to the real surface.
    hard_cut_enabled = bool(getattr(props, "dovetail_hard_side_cut", False)) or force_hard_cut
    clip_solid = None

    if hard_cut_enabled:
        clip_solid = _build_combined_solid_for_clip(a, b, cutters_coll)
        if clip_solid is None:
            report_user(None, 'WARNING',
                        'Hard-side cut: could not build combined surface (seam may not be closed); connector left untrimmed.')

    # Create dovetail with axis-relative dimensions and signed in-plane taper
    signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))
    ten = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                  length_v_mm=length_v_mm,
                                  depth_n_mm=depth_n_mm,
                                  signed_taper_pct=signed_taper,
                                  chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                                  name=f"{name_prefix}")
    ten.matrix_world = M
    cutters_coll.objects.link(ten)

    # Apply the chamfer bevel modifier now, before any boolean step below, so
    # the clip/union operations work on the already-chamfered mesh data
    # deterministically (same pattern as place_one_rect_tenon_at).
    for mod in list(ten.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = ten
            ten.select_set(True)
            try:
                apply_modifier_data(ten, mod)  # replaces the modifier_apply operator

            except Exception as e:
                report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
            ten.select_set(False)

    # Clip the tenon against the real object surface instead of AABB slabs
    if clip_solid is not None:
        ok = _clip_helper_to_combined_surface(ten, clip_solid)
        if not ok:
            report_user(None, 'WARNING',
                        'Hard-side cut failed on the connector; keeping untrimmed connector geometry.')

    # UNION into B
    union_and_dispose(b, ten, name=f"{name_prefix}_Union")


    # DIFFERENCE socket in A with XY (u/v) tolerance scaling
    mm = unit_mm()
    # Tolerance uses half of the smaller in-plane size to build a uniform scale in u/v
    half_min_plane = max(0.5 * min(width_u_mm, length_v_mm) * mm, 1e-9)
    s_inplane = 1.0 + (float(props.effective_tolerance()) * mm) / half_min_plane
    sx = s_inplane; sy = s_inplane; sz = 1.0

    # NEW: always enlarge the socket cutter's own u/v size by the fixed safety
    # overshoot BEFORE the tolerance scale is applied, so the cutter's side
    # faces genuinely overlap the target's outer wall instead of touching it
    # exactly. This is independent of dovetail_hard_side_cut and of tolerance.
    socket_width_u_mm, socket_length_v_mm = _uvn_socket_size_with_overshoot(width_u_mm, length_v_mm)

    socket = create_dovetail_box_uvn(width_u_mm=socket_width_u_mm,
                                     length_v_mm=socket_length_v_mm,
                                     depth_n_mm=depth_n_mm,
                                     signed_taper_pct=signed_taper,
                                     chamfer_mm=0.0,  # socket cutter stays sharp-edged; see DIFFERENCE note below
                                     name=f"{name_prefix}_SocketCutter")


    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)

    # NOTE: The socket cutter is intentionally NOT clipped against clip_solid.
    # It only feeds a DIFFERENCE operation, which already removes just the
    # material that geometrically overlaps A's real volume; excess cutter
    # geometry outside A's outer wall has no effect. Re-clipping it to the
    # exact combined surface (A union B) made its side faces coplanar with
    # A's own outer wall again, undoing the fixed u/v overshoot above and
    # causing the EXACT solver to leave a thin unremoved skin over the hole.
    # The tenon clip above is unaffected and remains required (visible
    # UNION geometry must not protrude past the real outer contour).

    cut_socket_with_cutter_and_dispose(a, socket)

    # Dispose the shared clip solid (still needed above for the tenon clip)
    if clip_solid is not None:
        _dispose_object(clip_solid, remove_data=True)

    if return_placement:
        # Return the final placement matrix and resolved axis-relative
        # dimensions so callers (e.g. the Snap Dovetail wrapper below) can
        # attach a sphere ring without duplicating the AUTO-span,
        # Forced-Span-Axis, and Signed-Taper resolution logic above.
        return M, width_u_mm, length_v_mm, depth_n_mm, signed_taper

    return None, None


# Click-placement wrapper for Snap Dovetail.

def place_one_snap_dovetail_at(a, b, axis, point_world, frame_z=None, props=None,
                                name_prefix="SnapDovetail_Click"):
    """Place one Snap Dovetail (tapered wedge + snap-sphere ring) at a world point.

    Delegates the full geometry pipeline (AUTO-span, Forced-Span-Axis,
    Hard-side Cut, Signed Taper) to place_one_dovetail_at(), then attaches a
    sphere ring sized to the real tapered side-wall width at the ring height —
    the same two-step pattern used for SNAP_PIN/SNAP_TENON in the modal
    LEFTMOUSE handler.
    """
    if props is None:
        props = bpy.context.scene.snapsplit

    placement = place_one_dovetail_at(
        a, b, axis, point_world,
        frame_z=frame_z, props=props,
        name_prefix=name_prefix,
        return_placement=True
    )
    M, width_u_mm, length_v_mm, depth_n_mm, signed_taper = placement
    if M is None:
        return None, None

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    add_snap_spheres_for_dovetail_ring(
        base_matrix=M,
        width_u_mm=width_u_mm,
        length_v_mm=length_v_mm,
        depth_n_mm=depth_n_mm,
        signed_taper_pct=signed_taper,
        props=props,
        name_prefix=name_prefix,
        part_a=a,   # A = DIFFERENCE
        part_b=b,   # B = UNION
        cutters_coll=cutters_coll
    )
    return None, None



# ---------------------------
# Placement & connect (pairwise seam plane)
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """Place connectors between adjacent parts along axis using LINE or GRID distribution."""
    if not parts:
        return []

    # 'axis' is only the fallback (scene Split Axis); each pair detects its own seam axis
    pairs = _build_connector_pairs(parts, axis, warn=True)
    if not pairs:
        return []


    # Validate the Custom Connector source object once, before processing any pairs/points,
    # to avoid repeating the same error report for every generated point.
    if getattr(props, "connector_type", ctype) == "CUSTOM":
        _custom_src = getattr(props, "custom_connector_object", None)
        if _custom_src is None or _custom_src.type != 'MESH' or _custom_src.data is None:
            report_user(None, 'ERROR',
                        'Please select a connector object for Custom Connector.')
            return []
        warn_if_unapplied_transforms(_custom_src)


    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # Robust axis unit vector with fallback to Z
    axis_map = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}
    naxis = axis_map.get(axis, Vector((0, 0, 1)))

    tol = float(props.effective_tolerance())
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    margin_pct = float(getattr(props, "connector_margin_pct", 10.0))
    cols = max(1, int(getattr(props, "connectors_per_seam", count)))

    for pair in pairs:
        a, b, axis, pair_seam_pos, pair_sign = pair[:5]
        # 6th element only exists for slanted seams: (origin, z pin->socket, in-plane tangent x)
        pair_plane = pair[5] if len(pair) > 5 else None
        x_hint = pair_plane[2] if pair_plane is not None else None

        # Per-pair seam axis (shadows the function argument on purpose, so all code
        # below that uses 'axis' and 'naxis' automatically works with the detected seam).
        # naxis points from B (pin) towards A (socket).
        naxis = axis_map[axis] * pair_sign
        if pair_plane is not None:
            naxis = pair_plane[1].copy()   # slanted seam: normal from B (pin) towards A (socket)
        seam_pos = pair_seam_pos if pair_seam_pos is not None else _pair_seam_plane_pos(a, b, axis, props)


        if pair_plane is not None:
            # Slanted seam: distribute inside the real contact patch
            points = distribute_points_on_plane(
                a, b, pair_plane, getattr(props, "connector_distribution", "LINE"),
                cols, max(1, int(getattr(props, "connectors_rows", 2))), margin_pct=margin_pct)
        elif getattr(props, "connector_distribution", "LINE") == "GRID":
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid_on_seam(a, b, cols, rows, axis, seam_pos, margin_pct=margin_pct)
        else:
            points = distribute_points_line_on_seam(a, b, cols, axis, seam_pos, margin_pct=margin_pct)



        ctype_for_pair = getattr(props, "connector_type", ctype)


        dovetail_span_axis_choice = str(getattr(props, "dovetail_span_axis", "NONE"))
        dovetail_span_role_pair = None
        dovetail_force_hard_cut_pair = False
        dovetail_span_axis_letter_pair = None  # resolved world axis letter (X/Y/Z) used for forced sizing
        if ctype_for_pair in {"DOVETAIL", "SNAP_DOVETAIL", "CUSTOM"}:
            x_pair, y_pair, z_pair = _orthonormal_frame_from_z(naxis, x_hint)

            dovetail_span_role_pair = _dovetail_span_axis_role(dovetail_span_axis_choice, x_pair, y_pair)
            if dovetail_span_role_pair == "U":
                dovetail_span_axis_letter_pair = (
                    dovetail_span_axis_choice if dovetail_span_axis_choice in {"X", "Y", "Z"}
                    else _world_axis_letter_from_direction(x_pair)
                )
                dovetail_force_hard_cut_pair = True
            elif dovetail_span_role_pair == "V":
                dovetail_span_axis_letter_pair = (
                    dovetail_span_axis_choice if dovetail_span_axis_choice in {"X", "Y", "Z"}
                    else _world_axis_letter_from_direction(y_pair)
                )
                dovetail_force_hard_cut_pair = True
            elif dovetail_span_axis_choice != "NONE" and dovetail_span_role_pair is None:
                report_user(None, 'WARNING',
                            'Selected Span Axis matches the seam normal, not the seam plane; span axis ignored.')

        dovetail_clip_solid = None
        if ctype_for_pair in {"DOVETAIL", "SNAP_DOVETAIL", "CUSTOM"} and (bool(getattr(props, "dovetail_hard_side_cut", False)) or dovetail_force_hard_cut_pair):
            dovetail_clip_solid = _build_combined_solid_for_clip(a, b, cutters_coll)
            if dovetail_clip_solid is None:
                report_user(None, 'WARNING',
                            'Hard-side cut: could not build combined surface (seam may not be closed); connector left untrimmed.')


        for i, p in enumerate(points):
            x, y, z = _orthonormal_frame_from_z(naxis, x_hint)


            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                L_scene = float(props.pin_length_mm) * unit_mm()
            elif ctype_cur in {"RECT_TENON", "SNAP_TENON", "DOVETAIL", "SNAP_DOVETAIL", "CUSTOM"}:
                # For dovetail in batch we will override depth_n via dovetail_depth_mm later
                L_scene = float(getattr(props, "tenon_depth_mm", 8.0)) * unit_mm()
            elif ctype_cur == "CUSTOM":
                L_scene = float(getattr(props, "custom_connector_depth_mm", 8.0)) * unit_mm()
            else:
                L_scene = float(props.tenon_depth_mm) * unit_mm()

            p_embed = p - z * (embed_pct * L_scene)

            M = Matrix((
                (x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0),
            ))

            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                seg = int(getattr(props, "pin_segments", 32))
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                     segments=seg, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)
                union_and_dispose(b, pin, name=f"PinUnion_{i}")

                mm = unit_mm()
                socket_d = float(props.pin_diameter_mm) + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

                if ctype_cur == "SNAP_PIN":
                    pin_radius_scene = 0.5 * float(props.pin_diameter_mm) * mm
                    length_scene = float(props.pin_length_mm) * mm
                    add_snap_spheres_for_cyl_pin(
                        base_matrix=M,
                        pin_radius_scene=pin_radius_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Pin_{i}",
                        part_a=a,  # A = DIFFERENCE
                        part_b=b,  # B = UNION
                        cutters_coll=cutters_coll
                    )

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            apply_modifier_data(tenon, mod)  # replaces the modifier_apply operator

                        except Exception as e:
                            report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
                        tenon.select_set(False)

                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0
                socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0,
                                                  name=f"TenonSocketCutter_{i}")
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

                if ctype_cur == "SNAP_TENON":
                    half_w_scene = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                    length_scene = float(props.tenon_depth_mm) * mm
                    add_snap_spheres_for_rect_tenon_ring(
                        base_matrix=M,
                        half_w_scene=half_w_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Tenon_{i}",
                        part_a=a,  # A = DIFFERENCE
                        part_b=b,  # B = UNION
                        cutters_coll=cutters_coll
                    )
            elif ctype_cur == "CUSTOM":
                source_obj = getattr(props, "custom_connector_object", None)
                if source_obj is None or source_obj.type != 'MESH' or source_obj.data is None:
                    report_user(None, 'ERROR', 'Please select a connector object for Custom Connector.')
                    created.append(None)
                    continue

                # Build a dedicated u/v/n frame, matching the DOVETAIL/SNAP_DOVETAIL
                # batch-path pattern, so Span Axis / Placement resolve consistently.
                x_c, y_c, z_c = _orthonormal_frame_from_z(naxis, x_hint)


                width_mm = float(getattr(props, "custom_connector_width_mm", 6.0))
                length_mm = float(getattr(props, "custom_connector_length_mm", 6.0))
                depth_mm = float(getattr(props, "custom_connector_depth_mm", 8.0))

                # Forced Span Axis override (reuses the pre-loop resolution above)
                if dovetail_span_role_pair == "U":
                    width_mm = _dovetail_forced_span_size_mm(a, b, dovetail_span_axis_letter_pair)
                elif dovetail_span_role_pair == "V":
                    length_mm = _dovetail_forced_span_size_mm(a, b, dovetail_span_axis_letter_pair)

                L_scene_c = depth_mm * unit_mm()
                p_embed_c = p - z_c * (embed_pct * L_scene_c)
                M_base_c = Matrix((
                    (x_c.x, y_c.x, z_c.x, p_embed_c.x),
                    (x_c.y, y_c.y, z_c.y, p_embed_c.y),
                    (x_c.z, y_c.z, z_c.z, p_embed_c.z),
                    (0,     0,     0,     1.0),
                ))
                Mc = _apply_inplane_offset_and_rotation(
                    M_base_c,
                    offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
                    offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
                    rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
                )

                conn = create_custom_connector_instance(source_obj, width_mm, length_mm, depth_mm,
                                                        chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                                                        name=f"Custom_{i}")
                if conn is None:
                    report_user(None, 'ERROR', 'Selected connector object has no usable mesh data.')
                    created.append(None)
                    continue
                conn.matrix_world = Mc
                cutters_coll.objects.link(conn)

                for mod in list(conn.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = conn
                        conn.select_set(True)
                        try:
                            apply_modifier_data(conn, mod)  # replaces the modifier_apply operator

                        except Exception as e:
                            report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
                        conn.select_set(False)

                if dovetail_clip_solid is not None:
                    ok = _clip_helper_to_combined_surface(conn, dovetail_clip_solid)
                    if not ok:
                        report_user(None, 'WARNING',
                                    'Hard-side cut failed on the connector; keeping untrimmed connector geometry.')

                union_and_dispose_safe(b, conn, name=f"CustomUnion_{i}", warn_label=f"Custom_{i}")

                mm = unit_mm()
                socket_width_mm, socket_length_mm = _uvn_socket_size_with_overshoot(width_mm, length_mm)
                half_w = max(0.5 * socket_width_mm * mm, 1e-9)
                half_l = max(0.5 * socket_length_mm * mm, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = 1.0 + (tol * mm) / half_l
                sz = 1.0
                socket = create_custom_connector_instance(source_obj, socket_width_mm, socket_length_mm, depth_mm,
                                                          chamfer_mm=0.0, name=f"CustomSocketCutter_{i}")
                socket.matrix_world = Mc @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose_safe(a, socket, warn_label=f"Custom_{i}")
                created.append(None)

                if bool(getattr(props, "custom_snap_spheres_enabled", False)):
                    half_w_scene = max(0.5 * width_mm * mm, 1e-9)
                    add_snap_spheres_for_rect_tenon_ring(
                        base_matrix=Mc,
                        half_w_scene=half_w_scene,
                        length_scene=depth_mm * mm,
                        props=props,
                        name_prefix=f"Custom_{i}",
                        part_a=a,
                        part_b=b,
                        cutters_coll=cutters_coll
                    )

            elif ctype_cur in {"DOVETAIL", "SNAP_DOVETAIL"}:
                # Build a dedicated local u/v/n frame for the dovetail, matching
                # the click-placement pipeline (place_one_dovetail_at).
                x_d, y_d, z_d = _orthonormal_frame_from_z(naxis, x_hint)


                # Frame at p with embed along depth_n
                depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))
                L_scene_dv = depth_n_mm * unit_mm()
                p_embed_dv = p - z_d * (embed_pct * L_scene_dv)

                M_base = Matrix((
                    (x_d.x, y_d.x, z_d.x, p_embed_dv.x),
                    (x_d.y, y_d.y, z_d.y, p_embed_dv.y),
                    (x_d.z, y_d.z, z_d.z, p_embed_dv.z),
                    (0,     0,     0,     1.0),
                ))

                # Apply in-plane controls (offsets along u/width and v/length, rotation)
                M2 = _apply_inplane_offset_and_rotation(
                    M_base,
                    offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
                    offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
                    rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
                )

                # Manual "Auto span along seam" checkbox (dovetail_auto_span), independent
                # from the dovetail_span_axis Forced Span Axis mechanism below.
                auto_span = bool(getattr(props, "dovetail_auto_span", False))
                margin_pct_dv = float(getattr(props, "dovetail_span_margin_pct", 10.0))

                width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
                length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))
                if auto_span:
                    span_u = _compute_edge_to_edge_span_along_dir(a, b, x_d, axis, seam_pos, margin_pct=margin_pct_dv)
                    span_v = _compute_edge_to_edge_span_along_dir(a, b, y_d, axis, seam_pos, margin_pct=margin_pct_dv)
                    width_u_mm = max(span_u / unit_mm(), 0.1)
                    length_v_mm = max(span_v / unit_mm(), 0.1)

                # Forced Span Axis override — reuses the pre-loop resolution computed
                # once per seam pair (dovetail_span_role_pair / dovetail_span_axis_letter_pair),
                # the same mechanism the CUSTOM branch above already uses. This is what
                # makes the "AUTO" default (Span Axis -> Dovetail Length/V axis) actually
                # execute for LINE/GRID batch placement.
                if dovetail_span_role_pair == "U":
                    width_u_mm = _dovetail_forced_span_size_mm(a, b, dovetail_span_axis_letter_pair)
                elif dovetail_span_role_pair == "V":
                    length_v_mm = _dovetail_forced_span_size_mm(a, b, dovetail_span_axis_letter_pair)

                signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))

                ten = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                              length_v_mm=length_v_mm,
                                              depth_n_mm=depth_n_mm,
                                              signed_taper_pct=signed_taper,
                                              chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                                              name=f"Dovetail_{i}")
                ten.matrix_world = M2
                cutters_coll.objects.link(ten)

                # Apply the chamfer bevel modifier now, before the hard-side clip
                # and the union below (same rationale as the click path).
                for mod in list(ten.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = ten
                        ten.select_set(True)
                        try:
                            apply_modifier_data(ten, mod)  # replaces the modifier_apply operator

                        except Exception as e:
                            report_user(None, 'WARNING', _trf('Bevel apply failure: {error}', error=e))
                        ten.select_set(False)

                # Hard-side cut clips against the pre-built combined surface
                # (dovetail_clip_solid is already built once per seam pair above).
                if dovetail_clip_solid is not None:
                    ok = _clip_helper_to_combined_surface(ten, dovetail_clip_solid)
                    if not ok:
                        report_user(None, 'WARNING',
                                    'Hard-side cut failed on the connector; keeping untrimmed connector geometry.')

                union_and_dispose(b, ten, name=f"DovetailUnion_{i}")

                # Socket with in-plane tolerance
                mm = unit_mm()
                half_min_plane = max(0.5 * min(width_u_mm, length_v_mm) * mm, 1e-9)
                s_inplane = 1.0 + (float(props.effective_tolerance()) * mm) / half_min_plane
                sx = s_inplane; sy = s_inplane; sz = 1.0

                # Always enlarge the socket cutter's own u/v size by the fixed
                # safety overshoot (same helper as the click-placement path), so
                # both interaction modes produce identical, reliable cuts.
                socket_width_u_mm, socket_length_v_mm = _uvn_socket_size_with_overshoot(width_u_mm, length_v_mm)

                socket = create_dovetail_box_uvn(width_u_mm=socket_width_u_mm,
                                                 length_v_mm=socket_length_v_mm,
                                                 depth_n_mm=depth_n_mm,
                                                 signed_taper_pct=signed_taper,
                                                 chamfer_mm=0.0,
                                                 name=f"DovetailSocketCutter_{i}")
                socket.matrix_world = M2 @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)

                # NOTE: No clip against dovetail_clip_solid for the socket cutter
                # (same rationale as place_one_dovetail_at): DIFFERENCE only
                # removes overlapping material, so leaving the overshoot-enlarged
                # cutter untrimmed avoids coplanar side faces with A's outer wall.

                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

                if ctype_cur == "SNAP_DOVETAIL":
                    add_snap_spheres_for_dovetail_ring(
                        base_matrix=M2,
                        width_u_mm=width_u_mm,
                        length_v_mm=length_v_mm,
                        depth_n_mm=depth_n_mm,
                        signed_taper_pct=signed_taper,
                        props=props,
                        name_prefix=f"Dovetail_{i}",
                        part_a=a,   # A = DIFFERENCE
                        part_b=b,   # B = UNION
                        cutters_coll=cutters_coll
                    )


            else:
                # Fallback -> behave like tenon
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)
                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0
                socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0,
                                                  name=f"TenonSocketCutter_{i}")
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

        # NEW: dispose the shared clip solid once this seam pair's connectors are done
        if dovetail_clip_solid is not None:
            _dispose_object(dovetail_clip_solid, remove_data=True)

    return created

# ---------------------------
# Live preview (LINE/GRID connector placement) — builder
# ---------------------------

def update_connector_placement_preview(context):
    """Create/refresh or remove the LINE/GRID connector placement live preview.

    Mirrors place_connectors_between()'s point distribution and per-point
    frame construction (same axis handling, seam-plane computation, and
    embed-depth math), but only creates lightweight WIRE preview objects
    (plus sphere-ring previews for SNAP_* types) instead of running any
    boolean union/socket operation. No hard-side clipping and no forced
    span-axis resizing are applied here, matching the existing behavior of
    the click-placement preview (SNAP_OT_place_connectors_click), so this
    stays a fast, side-effect-free visual approximation.
    """
    global _connector_preview_cap_warned
    try:
        scene = context.scene
        props = getattr(scene, "snapsplit", None)
        if not props:
            _clear_connector_placement_preview()
            return

        live = bool(getattr(props, "connector_live_preview", False))
        distribution = getattr(props, "connector_distribution", "LINE")
        sel = [o for o in context.selected_objects if o.type == 'MESH']

        # Guard: preview disabled, wrong distribution mode, or not enough parts
        if not live or distribution not in {"LINE", "GRID"} or len(sel) < 2:
            _clear_connector_placement_preview()
            return

        # Always rebuild from scratch so stale points/rings never linger
        _clear_connector_placement_preview()

        fallback_axis = getattr(props, "split_axis", "Z")
        pairs = _build_connector_pairs(sel, fallback_axis, warn=False)
        if not pairs:
            return

        ctype_cur = getattr(props, "connector_type", "CYL_PIN")

        # For CUSTOM, silently skip if no valid source object is picked yet
        # (mirrors the click-placement preview; avoids repeated error spam).
        if ctype_cur == "CUSTOM":
            source_obj = getattr(props, "custom_connector_object", None)
            if source_obj is None or source_obj.type != 'MESH' or source_obj.data is None:
                return

        prev_coll = ensure_collection("_SnapSplit_Preview")

        axis_map = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}

        embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
        margin_pct = float(getattr(props, "connector_margin_pct", 10.0))
        cols = max(1, int(getattr(props, "connectors_per_seam", 3)))
        mm = unit_mm()

        import math  # local import, consistent with the sphere-ring helpers above

        created_count = 0
        point_counter = 0
        cap_hit = False

        def _make_ring(base_matrix, ring_z, r_ring, d_sph_mm, name_base):
            """Create up to n_per_side wireframe sphere previews around a ring."""
            nonlocal created_count, cap_hit
            n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
            for k in range(n_per_side):
                if created_count >= AUTOPREVIEW_CAP:
                    cap_hit = True
                    return
                ang = (2.0 * math.pi) * (k / n_per_side)
                nx = math.cos(ang); ny = math.sin(ang)
                local_pos = Vector((r_ring * nx, r_ring * ny, ring_z))
                world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
                sph_prev = create_uv_sphere_preview(
                    d_mm=d_sph_mm, segments=12, rings=6,
                    name=f"{name_base}_Ring_{k}"
                )
                sph_prev.matrix_world = Matrix.Translation(Vector((world_pos.x, world_pos.y, world_pos.z)))
                prev_coll.objects.link(sph_prev)
                created_count += 1

        for pair in pairs:
            if cap_hit:
                break
            a, b, axis, pair_seam_pos, pair_sign = pair[:5]
            # 6th element only exists for slanted seams: (origin, z pin->socket, in-plane tangent x)
            pair_plane = pair[5] if len(pair) > 5 else None
            x_hint = pair_plane[2] if pair_plane is not None else None

            naxis = axis_map[axis] * pair_sign   # points from B (pin) towards A (socket)
            if pair_plane is not None:
                naxis = pair_plane[1].copy()   # slanted seam: normal from B (pin) towards A (socket)

            seam_pos = pair_seam_pos if pair_seam_pos is not None else _pair_seam_plane_pos(a, b, axis, props)


            if pair_plane is not None:
                # Slanted seam: distribute inside the real contact patch
                points = distribute_points_on_plane(
                    a, b, pair_plane, distribution,
                    cols, max(1, int(getattr(props, "connectors_rows", 2))), margin_pct=margin_pct)
            elif distribution == "GRID":
                rows = max(1, int(getattr(props, "connectors_rows", 2)))
                points = distribute_points_grid_on_seam(a, b, cols, rows, axis, seam_pos, margin_pct=margin_pct)
            else:
                points = distribute_points_line_on_seam(a, b, cols, axis, seam_pos, margin_pct=margin_pct)


            for p in points:
                if created_count >= AUTOPREVIEW_CAP:
                    cap_hit = True
                    break

                point_counter += 1
                name_base = f"{AUTOPREVIEW_PREFIX}{point_counter}"

                x, y, z = _orthonormal_frame_from_z(naxis, x_hint)


                # --- DOVETAIL / SNAP_DOVETAIL and CUSTOM: dedicated u/v/n frame + in-plane offset/rotation ---
                if ctype_cur in {"DOVETAIL", "SNAP_DOVETAIL", "CUSTOM"}:
                    width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
                    length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))
                    depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))
                    signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))

                    L_scene_dv = depth_n_mm * mm
                    p_embed_dv = p - z * (embed_pct * L_scene_dv)
                    M_base = Matrix((
                        (x.x, y.x, z.x, p_embed_dv.x),
                        (x.y, y.y, z.y, p_embed_dv.y),
                        (x.z, y.z, z.z, p_embed_dv.z),
                        (0,   0,   0,   1.0),
                    ))
                    M = _apply_inplane_offset_and_rotation(
                        M_base,
                        offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
                        offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
                        rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
                    )

                    dt_prev = create_dovetail_box_uvn(
                        width_u_mm=width_u_mm, length_v_mm=length_v_mm, depth_n_mm=depth_n_mm,
                        signed_taper_pct=signed_taper,
                        chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                        name=name_base
                    )
                    dt_prev.matrix_world = M
                    dt_prev.display_type = 'WIRE'
                    dt_prev.hide_select = True
                    prev_coll.objects.link(dt_prev)
                    created_count += 1

                    if ctype_cur == "SNAP_DOVETAIL" and created_count < AUTOPREVIEW_CAP:
                        d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                        protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                        depth_n_scene = max(0.1 * mm, depth_n_mm * mm)
                        width_u_scene = max(0.1 * mm, width_u_mm * mm)

                        zA = 0.5 * embed_pct * depth_n_scene
                        zB = _ring_height_for_visible_half(depth_n_scene, embed_pct)
                        ring_z = _choose_visible_half_robust(M, zA, zB)

                        # Same taper interpolation as add_snap_spheres_for_dovetail_ring(),
                        # so the ring sits on the real tapered side wall at ring_z.
                        t_prev = max(-90.0, min(90.0, signed_taper)) * 0.01
                        s_tip_prev = max(0.05, 1.0 - t_prev)
                        half_wb_u = 0.5 * width_u_scene
                        half_wt_u = max(0.05 * mm, half_wb_u * s_tip_prev)
                        frac = max(0.0, min(1.0, ring_z / depth_n_scene))
                        half_u_at_ring = half_wb_u + (half_wt_u - half_wb_u) * frac

                        sph_r_scene = 0.5 * d_sph_mm * mm
                        r_ring = half_u_at_ring + protr_scene - sph_r_scene
                        _make_ring(M, ring_z, r_ring, d_sph_mm, name_base)


                if ctype_cur == "CUSTOM":
                    source_obj = getattr(props, "custom_connector_object", None)
                    if source_obj is None or source_obj.type != 'MESH' or source_obj.data is None:
                        continue
                    width_mm = float(getattr(props, "custom_connector_width_mm", 6.0))
                    length_mm = float(getattr(props, "custom_connector_length_mm", 6.0))
                    depth_mm = float(getattr(props, "custom_connector_depth_mm", 8.0))

                    L_scene_c = depth_mm * mm
                    p_embed_c = p - z * (embed_pct * L_scene_c)
                    M_base_c = Matrix((
                        (x.x, y.x, z.x, p_embed_c.x),
                        (x.y, y.y, z.y, p_embed_c.y),
                        (x.z, y.z, z.z, p_embed_c.z),
                        (0,   0,   0,   1.0),
                    ))
                    Mc = _apply_inplane_offset_and_rotation(
                        M_base_c,
                        offset_u_mm=float(getattr(props, "dovetail_inplane_offset_u_mm", 0.0)),
                        offset_v_mm=float(getattr(props, "dovetail_inplane_offset_v_mm", 0.0)),
                        rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
                    )

                    custom_prev = create_custom_connector_instance(
                        source_obj, width_mm, length_mm, depth_mm,
                        chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                        name=name_base
                    )
                    if custom_prev is None:
                        continue
                    custom_prev.matrix_world = Mc
                    custom_prev.display_type = 'WIRE'
                    custom_prev.hide_select = True
                    prev_coll.objects.link(custom_prev)
                    created_count += 1

                    if bool(getattr(props, "custom_snap_spheres_enabled", False)) and created_count < AUTOPREVIEW_CAP:
                        d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                        protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                        half_w_scene = max(0.5 * width_mm * mm, 1e-9)

                        zA = 0.5 * embed_pct * L_scene_c
                        zB = _ring_height_for_visible_half(L_scene_c, embed_pct)
                        ring_z = _choose_visible_half_robust(Mc, zA, zB)
                        sph_r_scene = 0.5 * d_sph_mm * mm
                        r_ring = half_w_scene + protr_scene - sph_r_scene
                        _make_ring(Mc, ring_z, r_ring, d_sph_mm, name_base)

                    continue  # CUSTOM point fully handled



                # --- Non-dovetail types: shared x/y/z frame as in place_connectors_between ---
                if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                    L_scene = float(getattr(props, "pin_length_mm", 8.0)) * mm
                elif ctype_cur == "CUSTOM":
                    L_scene = float(getattr(props, "custom_connector_depth_mm", 8.0)) * mm
                else:
                    L_scene = float(getattr(props, "tenon_depth_mm", 8.0)) * mm

                p_embed = p - z * (embed_pct * L_scene)
                M = Matrix((
                    (x.x, y.x, z.x, p_embed.x),
                    (x.y, y.y, z.y, p_embed.y),
                    (x.z, y.z, z.z, p_embed.z),
                    (0,   0,   0,   1.0),
                ))

                wire_obj = None
                if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                    seg = int(getattr(props, "pin_segments", 32))
                    wire_obj = create_cyl_pin(
                        getattr(props, "pin_diameter_mm", 5.0),
                        getattr(props, "pin_length_mm", 8.0),
                        getattr(props, "add_chamfer_mm", 0.0),
                        segments=seg, name=name_base
                    )
                elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                    wire_obj = create_rect_tenon_quader(
                        getattr(props, "tenon_width_mm", 6.0),
                        getattr(props, "tenon_depth_mm", 8.0),
                        getattr(props, "add_chamfer_mm", 0.0),
                        name=name_base
                    )


                else:
                    # Fallback -> behave like tenon (mirrors place_connectors_between's fallback)
                    wire_obj = create_rect_tenon_quader(
                        getattr(props, "tenon_width_mm", 6.0),
                        getattr(props, "tenon_depth_mm", 8.0),
                        getattr(props, "add_chamfer_mm", 0.0),
                        name=name_base
                    )

                if wire_obj is None:
                    # e.g. CUSTOM with a source object that has no usable mesh data
                    continue

                wire_obj.matrix_world = M
                wire_obj.display_type = 'WIRE'
                wire_obj.hide_select = True
                prev_coll.objects.link(wire_obj)
                created_count += 1

                if ctype_cur == "SNAP_PIN" and created_count < AUTOPREVIEW_CAP:
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    pin_radius_scene = 0.5 * float(getattr(props, "pin_diameter_mm", 5.0)) * mm

                    zA = 0.5 * embed_pct * L_scene
                    zB = _ring_height_for_visible_half(L_scene, embed_pct)
                    ring_z = _choose_visible_half_robust(M, zA, zB)
                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_ring = pin_radius_scene + protr_scene - sph_r_scene
                    _make_ring(M, ring_z, r_ring, d_sph_mm, name_base)

                elif ctype_cur == "SNAP_TENON" and created_count < AUTOPREVIEW_CAP:
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    half_w_scene = 0.5 * float(getattr(props, "tenon_width_mm", 6.0)) * mm

                    zA = 0.5 * embed_pct * L_scene
                    zB = _ring_height_for_visible_half(L_scene, embed_pct)
                    ring_z = _choose_visible_half_robust(M, zA, zB)
                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_ring = half_w_scene + protr_scene - sph_r_scene
                    _make_ring(M, ring_z, r_ring, d_sph_mm, name_base)

        # Report the cap only once while it stays hit; reset once we drop below it again
        if cap_hit:
            if not _connector_preview_cap_warned:
                report_user(None, 'WARNING',
                            _trf('Connector live preview stopped at {cap} objects; remaining points are not shown.', cap=AUTOPREVIEW_CAP))
                _connector_preview_cap_warned = True
        else:
            _connector_preview_cap_warned = False

    except Exception:
        # Never break UI interactions if the preview builder raises under an unusual context state
        pass



# ---------------------------
# Modal operator: place by click (pins or tenons or dovetail)
# ---------------------------

class SNAP_OT_place_connectors_click(Operator):
    """Interactively place a connector (pin/tenon/dovetail) by clicking on the seam plane between two parts."""
    bl_idname = "snapsplit.place_connectors_click"
    bl_label = "Place connectors (click)"
    bl_description = "Interactively place a connector (pin/tenon/dovetail) by clicking on the seam plane between two parts."
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        """Start modal placement with live preview for two selected mesh parts."""
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) != 2:
            report_user(self, 'ERROR',
                        'Select exactly 2 adjacent split parts.')
            return {'CANCELLED'}

        self.props = props

        # Detect seam axis, roles (A = socket, B = pin) and insertion direction from geometry
        resolved = _resolve_pair(sel[0], sel[1])
        # Slanted seam data; stays None for axis-parallel seams and for the fallback
        self.plane_center = None
        self.frame_x = None
        slanted_plane = None
        if resolved is not None:
            # Slice: resolved has 6 elements for slanted seams
            self.a, self.b, self.axis, self.seam_pos, sign = resolved[:5]
            slanted_plane = resolved[5] if len(resolved) > 5 else None
        else:
            report_user(
                self,
                'ERROR',
                "No shared planar contact area was found. "
                "Select two parts that currently touch face-to-face.",
            )
            return {'CANCELLED'}


        # Insertion direction (points from B (pin) towards A (socket)); used by preview and placement

        self.frame_z = _axis_unit_vector(self.axis) * sign
        if slanted_plane is not None:
            # Slanted seam: insertion direction and in-plane tangent come from the seam plane
            origin_s, z_s, x_s = slanted_plane
            self.frame_z = z_s.copy()
            self.frame_x = x_s.copy()
            patch_s = _slanted_contact_patch(self.a, self.b, origin_s, z_s, x_s)
            # The mouse ray is intersected with this plane (point inside the contact patch)
            self.plane_center = patch_s[0] if patch_s is not None else origin_s.copy()

        # Show the placement preview through solid objects in the clicked viewport.
        # Released in finish() (ESC / right click).
        xray_acquire(context, "click_place")


        try:
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            prev_coll = ensure_collection("_SnapSplit_Preview")

            self.preview_objs = []
            self.preview_obj = None

            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                # Pin preview: the whole wireframe setup belongs to the pin types only
                seg = int(getattr(props, "pin_segments", 32))
                pin_prev = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                          segments=seg, name="SnapSplit_Preview_Conn")
                pin_prev.display_type = 'WIRE'
                pin_prev.hide_select = True
                prev_coll.objects.link(pin_prev)
                self.preview_obj = pin_prev
                self.preview_objs.append(pin_prev)


            if ctype_cur == "SNAP_PIN":
                # Show sphere ring preview
                mm = unit_mm()
                n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                pin_radius_scene = 0.5 * float(props.pin_diameter_mm) * mm
                length_scene = float(props.pin_length_mm) * mm

                embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                L_free = max(0.0, (1.0 - embed_pct) * length_scene)
                zA = 0.5 * embed_pct * length_scene
                zB = embed_pct * length_scene + 0.5 * L_free

                sph_r_scene = 0.5 * d_sph_mm * mm
                r_center = pin_radius_scene + protr_scene - sph_r_scene

                import math
                for i in range(n_per_side):
                    ang = (2.0 * math.pi) * (i / n_per_side)
                    nx = math.cos(ang); ny = math.sin(ang)
                    local_A = (r_center * nx, r_center * ny, zA)
                    local_B = (r_center * nx, r_center * ny, zB)
                    sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                        name=f"SnapSplit_Preview_Snap_{i}")
                    sph_prev["_snapsplit_local_offset_A"] = local_A
                    sph_prev["_snapsplit_local_offset_B"] = local_B
                    prev_coll.objects.link(sph_prev)
                    self.preview_objs.append(sph_prev)

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON", "DOVETAIL", "SNAP_DOVETAIL", "CUSTOM"}:
                if ctype_cur in {"DOVETAIL", "SNAP_DOVETAIL"}:
                    # Dovetail preview uses axis-relative dimensions and signed in-plane taper
                    width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
                    length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))
                    depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))
                    signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))
                    ten_prev = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                                       length_v_mm=length_v_mm,
                                                       depth_n_mm=depth_n_mm,
                                                       signed_taper_pct=signed_taper,
                                                       chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                                                       name="SnapSplit_Preview_Dovetail")

                elif ctype_cur == "CUSTOM":
                    source_obj = getattr(props, "custom_connector_object", None)
                    if source_obj is not None and source_obj.type == 'MESH' and source_obj.data is not None:
                        width_mm = float(getattr(props, "custom_connector_width_mm", 6.0))
                        length_mm = float(getattr(props, "custom_connector_length_mm", 6.0))
                        depth_mm = float(getattr(props, "custom_connector_depth_mm", 8.0))


                        custom_prev = create_custom_connector_instance(
                            source_obj, width_mm, length_mm, depth_mm,
                            chamfer_mm=float(getattr(props, "add_chamfer_mm", 0.0)),
                            name="SnapSplit_Preview_Custom"
                        )
                        if custom_prev is not None:
                            custom_prev.display_type = 'WIRE'
                            custom_prev.hide_select = True
                            prev_coll.objects.link(custom_prev)
                            self.preview_obj = custom_prev
                            self.preview_objs.append(custom_prev)
                    # If no source object is picked yet, silently skip the preview here;
                    # the actual LEFTMOUSE placement already reports a clear error in that case.

                # NEW: insert this block directly after the existing
                # "if ctype_cur == \"SNAP_TENON\": ..." block (same indentation level),
                # so it follows the identical local-offset-tag pattern used there.
                if ctype_cur == "CUSTOM" and bool(getattr(props, "custom_snap_spheres_enabled", False)):
                    mm = unit_mm()
                    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    half_w_scene = 0.5 * float(getattr(props, "custom_connector_width_mm", 6.0)) * mm
                    length_scene = float(getattr(props, "custom_connector_depth_mm", 8.0)) * mm

                    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
                    zA = 0.5 * embed_pct * length_scene
                    zB = embed_pct * length_scene + 0.5 * L_free

                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_center = half_w_scene + protr_scene - sph_r_scene

                    import math
                    for i in range(n_per_side):
                        ang = (2.0 * math.pi) * (i / n_per_side)
                        nx = math.cos(ang); ny = math.sin(ang)
                        local_A = (r_center * nx, r_center * ny, zA)
                        local_B = (r_center * nx, r_center * ny, zB)
                        sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                            name=f"SnapSplit_Preview_SnapCustom_{i}")
                        sph_prev["_snapsplit_local_offset_A"] = local_A
                        sph_prev["_snapsplit_local_offset_B"] = local_B
                        prev_coll.objects.link(sph_prev)
                        self.preview_objs.append(sph_prev)

                # Rectangular preview box only for the tenon types.
                # (Dovetail already created its own ten_prev above; Custom has its own preview.)
                if ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                    ten_prev = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                        name="SnapSplit_Preview_Conn")


                # IMPORTANT: the CUSTOM branch above already fully sets up (or
                # intentionally skips) its own preview object and never assigns
                # ten_prev. Running this unconditionally for CUSTOM raised a
                # NameError, silently swallowed by the outer try/except, which
                # then reset self.preview_obj/self.preview_objs to None/[] and
                # discarded the already-created custom_prev reference.
                if ctype_cur != "CUSTOM":
                    ten_prev.display_type = 'WIRE'
                    ten_prev.hide_select = True
                    prev_coll.objects.link(ten_prev)
                    self.preview_obj = ten_prev
                    self.preview_objs.append(ten_prev)


                if ctype_cur == "SNAP_TENON":
                    mm = unit_mm()
                    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    half_w_scene = 0.5 * float(props.tenon_width_mm) * mm
                    length_scene = float(props.tenon_depth_mm) * mm

                    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
                    zA = 0.5 * embed_pct * length_scene
                    zB = embed_pct * length_scene + 0.5 * L_free

                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_center = half_w_scene + protr_scene - sph_r_scene

                    import math
                    for i in range(n_per_side):
                        ang = (2.0 * math.pi) * (i / n_per_side)
                        nx = math.cos(ang); ny = math.sin(ang)
                        local_A = (r_center * nx, r_center * ny, zA)
                        local_B = (r_center * nx, r_center * ny, zB)
                        sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                            name=f"SnapSplit_Preview_SnapTen_{i}")
                        sph_prev["_snapsplit_local_offset_A"] = local_A
                        sph_prev["_snapsplit_local_offset_B"] = local_B
                        prev_coll.objects.link(sph_prev)
                        self.preview_objs.append(sph_prev)

                if ctype_cur == "SNAP_DOVETAIL":
                    mm = unit_mm()
                    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

                    depth_n_scene = max(0.1 * mm, depth_n_mm * mm)
                    width_u_scene = max(0.1 * mm, width_u_mm * mm)

                    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                    L_free = max(0.0, (1.0 - embed_pct) * depth_n_scene)
                    zA = 0.5 * embed_pct * depth_n_scene
                    zB = embed_pct * depth_n_scene + 0.5 * L_free

                    # Same taper interpolation as add_snap_spheres_for_dovetail_ring(),
                    # evaluated separately at zA and zB since the tapered radius
                    # differs between the embedded and the protruding half.
                    t_prev = max(-90.0, min(90.0, signed_taper)) * 0.01
                    s_tip_prev = max(0.05, 1.0 - t_prev)
                    half_wb_u = 0.5 * width_u_scene
                    half_wt_u = max(0.05 * mm, half_wb_u * s_tip_prev)

                    def _half_u_at(z, _wb=half_wb_u, _wt=half_wt_u, _dn=depth_n_scene):
                        frac = max(0.0, min(1.0, z / _dn))
                        return _wb + (_wt - _wb) * frac

                    sph_r_scene = 0.5 * d_sph_mm * mm

                    import math
                    for i in range(n_per_side):
                        ang = (2.0 * math.pi) * (i / n_per_side)
                        nx = math.cos(ang); ny = math.sin(ang)
                        r_A = _half_u_at(zA) + protr_scene - sph_r_scene
                        r_B = _half_u_at(zB) + protr_scene - sph_r_scene
                        local_A = (r_A * nx, r_A * ny, zA)
                        local_B = (r_B * nx, r_B * ny, zB)
                        sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                            name=f"SnapSplit_Preview_SnapDvt_{i}")
                        sph_prev["_snapsplit_local_offset_A"] = local_A
                        sph_prev["_snapsplit_local_offset_B"] = local_B
                        prev_coll.objects.link(sph_prev)
                        self.preview_objs.append(sph_prev)

        except Exception:
            # Print the error to the console instead of hiding it; placing by click still works
            import traceback
            traceback.print_exc()
            self.preview_obj = None
            self.preview_objs = []


        # Key hints in the status bar; reset in finish()
        self.roles_flipped_live = False
        self._update_status_text(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):

        """Tear down preview objects and collections; also remove cutters collection on cancel or end."""
        # Restore the X-Ray state saved in invoke() (no-op if nothing was acquired)
        xray_release("click_place")
        # Restore the default status bar text
        try:
            context.workspace.status_text_set(None)
        except Exception:
            pass

        try:
            to_purge = set()

            if getattr(self, "preview_obj", None) and self.preview_obj.name in bpy.data.objects:
                to_purge.add(bpy.data.objects.get(self.preview_obj.name))
            if getattr(self, "preview_objs", None):
                for o in list(self.preview_objs):
                    if o and o.name in bpy.data.objects:
                        to_purge.add(bpy.data.objects.get(o.name))

            prev_coll = bpy.data.collections.get("_SnapSplit_Preview")
            name_prefixes = (
                "SnapSplit_Preview_",
                "SnapSplit_Preview_Snap_",
                "SnapSplit_Preview_SnapTen_",
                "SnapSplit_Preview_SnapDvt_",
                "SnapSplit_Preview_Conn",
                "SnapSplit_Preview_Dovetail",
            )
            if prev_coll:
                for o in list(prev_coll.objects):
                    try:
                        if (o.name.startswith(name_prefixes)) or bool(o.get("_snapsplit_preview")):
                            to_purge.add(o)
                    except Exception:
                        pass

            for o in list(bpy.data.objects):
                try:
                    if (o.name.startswith(name_prefixes)) or bool(o.get("_snapsplit_preview")):
                        to_purge.add(o)
                except Exception:
                    pass

            for obj in list(to_purge):
                if not obj:
                    continue
                try:
                    for coll in list(obj.users_collection):
                        try:
                            coll.objects.unlink(obj)
                        except Exception:
                            pass
                except Exception:
                    pass

                mesh_data = getattr(obj, "data", None)

                try:
                    bpy.data.objects.remove(obj)
                except Exception:
                    try:
                        _dispose_object(obj, remove_data=False)
                    except Exception:
                        pass

                try:
                    if mesh_data and hasattr(mesh_data, "users") and mesh_data.users == 0:
                        if mesh_data.__class__.__name__ == "Mesh":
                            bpy.data.meshes.remove(mesh_data)
                        else:
                            bpy.data.batch_remove((mesh_data,))
                except Exception:
                    pass

            try:
                if prev_coll:
                    for parent in list(bpy.data.collections):
                        try:
                            if prev_coll.name in [c.name for c in getattr(parent, "children", [])]:
                                parent.children.unlink(prev_coll)
                        except Exception:
                            pass
                    try:
                        scene_root = bpy.context.view_layer.layer_collection.collection
                        if prev_coll.name in [c.name for c in scene_root.children]:
                            scene_root.children.unlink(prev_coll)
                    except Exception:
                        pass
                    try:
                        bpy.data.collections.remove(prev_coll)
                    except Exception:
                        pass
            except Exception:
                pass

            try:
                if getattr(self, "preview_objs", None) is not None:
                    self.preview_objs.clear()
            except Exception:
                pass
            self.preview_obj = None

            try:
                context.view_layer.update()
            except Exception:
                pass

        except Exception:
            pass

        try:
            remove_cutters_collection()
        except Exception:
            pass

        if cancelled:
            report_user(self, 'INFO', 'Placement cancelled.')

    def modal(self, context, event):
        """Handle mouse movement for preview updates and left-click for placement."""
        try:
            if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

            # Key S: swap pin / socket while placing. Key repeat and modifier combos
            # (e.g. Ctrl+S) are ignored so nothing toggles by accident.
            swapped_now = False
            if (event.type == 'S' and event.value == 'PRESS'
                    and not getattr(event, "is_repeat", False)
                    and not (event.ctrl or event.alt or event.shift or event.oskey)):
                self._toggle_roles_now(context)
                swapped_now = True

            # After a swap the existing preview code runs once with the last mouse position,
            # so the preview flips immediately without moving the mouse.
            if event.type == 'MOUSEMOVE' or swapped_now:
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        M = self._build_frame_at(hit)
                        if self.preview_obj:

                            ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                            # For dovetail previews, apply in-plane offsets (width/length) + rotation so preview == result
                            if ctype_cur in {"DOVETAIL", "SNAP_DOVETAIL"}:
                                M = _apply_inplane_offset_and_rotation(
                                    M,
                                    offset_u_mm=float(getattr(self.props, "dovetail_inplane_offset_u_mm", 0.0)),
                                    offset_v_mm=float(getattr(self.props, "dovetail_inplane_offset_v_mm", 0.0)),
                                    rotation_deg=float(getattr(self.props, "dovetail_inplane_rotation_deg", 0.0))
                                )

                            self.preview_obj.matrix_world = M

                        if getattr(self, "preview_objs", None) and len(self.preview_objs) > 1:
                            try:
                                z_axis_world = Vector((M[0][2], M[1][2], M[2][2])).normalized()
                            except Exception:
                                z_axis_world = None
                            for o in self.preview_objs:
                                if o is self.preview_obj:
                                    continue
                                try:
                                    if "_snapsplit_local_offset_B" in o:
                                        oxA, oyA, ozA = o.get("_snapsplit_local_offset_A", (0.0, 0.0, 0.0))
                                        oxB, oyB, ozB = o.get("_snapsplit_local_offset_B", (0.0, 0.0, 0.0))
                                        if z_axis_world is not None:
                                            pA_w_v = (M @ Vector((oxA, oyA, ozA, 1.0)))
                                            pB_w_v = (M @ Vector((oxB, oyB, ozB, 1.0)))
                                            dA = Vector((pA_w_v.x, pA_w_v.y, pA_w_v.z)).dot(z_axis_world)
                                            dB = Vector((pB_w_v.x, pB_w_v.y, pB_w_v.z)).dot(z_axis_world)
                                            use_B = dB >= dA
                                        else:
                                            use_B = True
                                        o.matrix_world = M @ Matrix.Translation((oxB, oyB, ozB)) if use_B else M @ Matrix.Translation((oxA, oyA, ozA))
                                except Exception:
                                    pass
                except Exception:
                    pass
                return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                        fz = self.frame_z  # insertion direction B (pin) -> A (socket)
                        # place_one_*_at() build their own frame; give them the seam tangent
                        _set_frame_x_hint(getattr(self, "frame_x", None))

                        if ctype_cur == "CYL_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Pin_Click")
                        elif ctype_cur == "RECT_TENON":
                            place_one_rect_tenon_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Tenon_Click")
                        elif ctype_cur == "SNAP_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Pin_Click")
                            M = self._build_frame_at(hit)
                            mm = unit_mm()
                            pin_radius_scene = 0.5 * float(self.props.pin_diameter_mm) * mm
                            length_scene = float(self.props.pin_length_mm) * mm
                            cutters_coll = ensure_collection("_SnapSplit_Cutters")
                            add_snap_spheres_for_cyl_pin(
                                base_matrix=M,
                                pin_radius_scene=pin_radius_scene,
                                length_scene=length_scene,
                                props=self.props,
                                name_prefix="Pin_Click",
                                part_a=self.a,  # A = DIFFERENCE
                                part_b=self.b,  # B = UNION
                                cutters_coll=cutters_coll
                            )
                        elif ctype_cur == "SNAP_TENON":
                            place_one_rect_tenon_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Tenon_Click")
                            M = self._build_frame_at(hit)
                            mm = unit_mm()
                            half_w_scene = 0.5 * float(self.props.tenon_width_mm) * mm
                            length_scene = float(self.props.tenon_depth_mm) * mm
                            cutters_coll = ensure_collection("_SnapSplit_Cutters")
                            add_snap_spheres_for_rect_tenon_ring(
                                base_matrix=M,
                                half_w_scene=half_w_scene,
                                length_scene=length_scene,
                                props=self.props,
                                name_prefix="Tenon_Click",
                                part_a=self.a,  # A = DIFFERENCE
                                part_b=self.b,  # B = UNION
                                cutters_coll=cutters_coll
                            )
                        elif ctype_cur == "DOVETAIL":
                            place_one_dovetail_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Dovetail_Click")
                        elif ctype_cur == "SNAP_DOVETAIL":
                            place_one_snap_dovetail_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="SnapDovetail_Click")
                        elif ctype_cur == "CUSTOM":
                            place_one_custom_connector_at(self.a, self.b, self.axis, hit, frame_z=fz, props=self.props, name_prefix="Custom_Click")


                        try:
                            remove_cutters_collection()
                        except Exception:
                            pass

                except Exception as e:
                    report_user(self, 'ERROR',
                                _trf('Placement failed: {error}', error=e))
                finally:
                    # Always clear the tangent hint so later calls use the world-X based frame
                    _set_frame_x_hint(None)
                return {'RUNNING_MODAL'}


            return {'RUNNING_MODAL'}

        except Exception as e:
            report_user(self, 'ERROR', _trf('Modal error: {error}', error=e))
            return {'RUNNING_MODAL'}

    def _update_status_text(self, context):
        """Show the key hints (and the live role state) in the Blender status bar."""
        try:
            state = "swapped" if getattr(self, "roles_flipped_live", False) else "default"
            context.workspace.status_text_set(
                f"S: swap pin / socket ({state})  |  LMB: place  |  RMB / Esc: cancel")
        except Exception:
            pass

    def _toggle_roles_now(self, context):
        """Swap pin and socket during placement (key S).

        Same effect as the 'Swap Pin / Socket' panel switch (see _swap_roles()):
        A and B are exchanged and the insertion direction frame_z is inverted.
        The in-plane tangent frame_x of a slanted seam stays unchanged.
        The panel property is NOT touched on purpose: changing it would fire the live
        preview update callback while this modal operator owns the preview objects.
        """
        self.a, self.b = self.b, self.a
        self.frame_z = -self.frame_z
        self.roles_flipped_live = not getattr(self, "roles_flipped_live", False)
        self._update_status_text(context)


    def _intersect_mouse_with_seam_plane(self, context, event):
        """Raycast from mouse into the seam plane and return the hit point in world space."""
        n = {
            "X": Vector((1, 0, 0)),
            "Y": Vector((0, 1, 0)),
            "Z": Vector((0, 0, 1)),
        }.get(self.axis, Vector((0, 0, 1))).normalized()

        ca = sum([self.a.matrix_world @ Vector(c) for c in self.a.bound_box], Vector()) / 8.0
        cb = sum([self.b.matrix_world @ Vector(c) for c in self.b.bound_box], Vector()) / 8.0
        c = 0.5 * (ca + cb)
        idx = _axis_index(self.axis)
        c[idx] = self.seam_pos
        plane_point = c
        plane_normal = n
        # Slanted seam: use the real plane (contact patch center + seam normal)
        if getattr(self, "plane_center", None) is not None:
            plane_point = self.plane_center
            plane_normal = self.frame_z.normalized()


        region = context.region
        rv3d = context.region_data
        if not rv3d:
            return None
        mx, my = event.mouse_region_x, event.mouse_region_y
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (mx, my))
        view_vec = rv3d.view_rotation @ Vector((0.0, 0.0, -1.0))
        ray_target = view3d_utils.region_2d_to_location_3d(region, rv3d, (mx, my), view_vec)
        ray_dir = (ray_target - ray_origin).normalized()

        denom = ray_dir.dot(plane_normal)
        if abs(denom) < 1e-8:
            return None
        t = (plane_point - ray_origin).dot(plane_normal) / denom
        if t < 0:
            return None
        return ray_origin + ray_dir * t

    def _build_frame_at(self, point_world):
        """Build a local placement frame (Matrix) at a world point based on axis and embed depth.

        Note: For preview, we use tenon_depth_mm by legacy for non-dovetail types.
        Dovetail placement later overrides depth with dovetail_depth_mm.
        """
        # Uses the in-plane tangent of a slanted seam if there is one (frame_x is None otherwise)
        x, y, z = _orthonormal_frame_from_z(self.frame_z, getattr(self, "frame_x", None))


        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
        if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
            L_scene = float(self.props.pin_length_mm) * unit_mm()
        elif ctype_cur in {"DOVETAIL", "SNAP_DOVETAIL"}:
            L_scene = float(getattr(self.props, "dovetail_depth_mm", 8.0)) * unit_mm()
        elif ctype_cur == "CUSTOM":
            # Use the Custom Connector's own depth so the preview/embed offset
            # matches the actual placement in place_one_custom_connector_at().
            L_scene = float(getattr(self.props, "custom_connector_depth_mm", 8.0)) * unit_mm()
        else:
            L_scene = float(getattr(self.props, "tenon_depth_mm", 8.0)) * unit_mm()


        embed_pct = float(getattr(self.props, "pin_embed_pct", 50.0)) * 0.01
        p_embed = point_world - z * (embed_pct * L_scene)

        return Matrix((
            (x.x, y.x, z.x, p_embed.x),
            (x.y, y.y, z.y, p_embed.y),
            (x.z, y.z, z.z, p_embed.z),
            (0,   0,   0,   1.0),
        ))


# ---------------------------
# Batch placement operator (existing)
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    """Batch-place connectors between all adjacent selected parts using current settings."""
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors"
    bl_description = "Batch-place connectors between all adjacent selected parts using current settings."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute batch placement for selected mesh parts."""
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR',
                        'Select at least 2 cut mesh-pieces.')
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis=props.split_axis,
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )

        try:
            remove_cutters_collection()
        except Exception:
            pass

        report_user(self, 'INFO',
                    _trf('{value} connectors created.', value=len(created)))
        return {'FINISHED'}


# ---------------------------
# Registration
# ---------------------------

classes = (SNAP_OT_add_connectors, SNAP_OT_place_connectors_click)

def register():
    """Register operators for connector placement."""
    # Labels and descriptions are plain class attributes; Blender translates them itself.
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    """Unregister operators for connector placement."""
    # Ensure no leftover live-preview objects survive an addon disable/reload
    _clear_connector_placement_preview()
    for c in reversed(classes):
        bpy.utils.unregister_class(c)



```

---

### ops_freehand.py

```py
'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''
"""Freehand Cut, stage A: non-destructive stroke and section preview."""

# ops_freehand.py

import hashlib
import math

from array import array
from datetime import datetime

import bpy
import bmesh
import gpu

from bpy.props import FloatProperty
from bpy.types import Operator
from bpy_extras import view3d_utils
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from .utils import report_user
from .ops_split import warn_if_unapplied_transforms
from .seam_data import write_freehand_seams
from .seam_migration import migrate_intact_freehand_seams




# The brush remains an operator property rather than a persistent scene property.
DEFAULT_BRUSH_RADIUS = 10.0
SAMPLE_SPACING = 6.0
MAX_SAMPLES = 200
MAX_STROKE_POINTS = 4096

PARTS_COLLECTION_NAME = "SnapSplit_Parts"

ORANGE = (1.0, 0.35, 0.04, 1.0)
GRAY = (0.48, 0.52, 0.58, 0.75)
INVALID_COLOR = (1.0, 0.15, 0.12, 0.9)

_ACTIVE_OPERATORS = []


# ---------------------------------------------------------------------------
# Source validation
# ---------------------------------------------------------------------------

def _geometry_signature(mesh):
    """Hash vertex coordinates and topology independently of element counts."""
    digest = hashlib.sha256()

    specifications = (
        (mesh.vertices, "co", "f", 3),
        (mesh.edges, "vertices", "i", 2),
        (mesh.loops, "vertex_index", "i", 1),
        (mesh.polygons, "loop_start", "i", 1),
        (mesh.polygons, "loop_total", "i", 1),
    )

    for collection, attribute, typecode, width in specifications:
        values = array(typecode, [0]) * (len(collection) * width)
        collection.foreach_get(attribute, values)
        digest.update(len(values).to_bytes(8, "little"))
        digest.update(values.tobytes())

    return digest.digest()


# ---------------------------------------------------------------------------
# Stroke and plane utilities
# ---------------------------------------------------------------------------

def _resample_stroke(points):
    """Resample the complete stroke uniformly, including both endpoints."""
    if len(points) < 2:
        return list(points)

    lengths = [0.0]
    for a, b in zip(points, points[1:]):
        lengths.append(lengths[-1] + (b - a).length)

    total = lengths[-1]
    if total <= 1e-8:
        return [points[0].copy()]

    count = min(
        MAX_SAMPLES,
        max(2, math.ceil(total / SAMPLE_SPACING) + 1),
    )
    result = []
    segment = 0

    for i in range(count):
        distance = total * i / (count - 1)

        while (
            segment < len(points) - 2
            and lengths[segment + 1] < distance
        ):
            segment += 1

        span = lengths[segment + 1] - lengths[segment]
        factor = (
            (distance - lengths[segment]) / span
            if span > 1e-8
            else 0.0
        )
        result.append(
            points[segment].lerp(points[segment + 1], factor)
        )

    return result


def _fit_line(points):
    """Return the centroid and endpoint pair of the dominant 2D PCA axis."""
    if len(points) < 2:
        raise ValueError("Draw a longer stroke.")

    center = sum(points, Vector((0.0, 0.0))) / len(points)

    xx = yy = xy = 0.0
    for point in points:
        delta = point - center
        xx += delta.x * delta.x
        yy += delta.y * delta.y
        xy += delta.x * delta.y

    trace = xx + yy
    difference = math.hypot(xx - yy, 2.0 * xy)

    if trace <= 1e-8 or difference <= trace * 1e-6:
        raise ValueError(
            "The stroke has no clear direction. Draw a straighter line."
        )

    angle = 0.5 * math.atan2(2.0 * xy, xx - yy)
    direction = Vector((math.cos(angle), math.sin(angle)))
    positions = [
        (point - center).dot(direction)
        for point in points
    ]

    low = min(positions)
    high = max(positions)

    if high - low < 8.0:
        raise ValueError("Draw a stroke at least 8 pixels long.")

    return (
        center,
        center + direction * low,
        center + direction * high,
    )


def _plane_basis(normal):
    """Build an orthonormal basis on a plane."""
    helper = Vector((0.0, 0.0, 1.0))
    if abs(normal.dot(helper)) > 0.9:
        helper = Vector((0.0, 1.0, 0.0))

    u = normal.cross(helper).normalized()
    v = normal.cross(u).normalized()
    return u, v


def _point_segment_distance(point, a, b):
    """Return the Euclidean distance from a point to a segment."""
    delta = b - a
    denominator = delta.length_squared

    if denominator <= 1e-20:
        return (point - a).length

    factor = max(
        0.0,
        min(1.0, (point - a).dot(delta) / denominator),
    )
    return (point - (a + factor * delta)).length


def _polygon_distance(point, polygon):
    """Return the distance to the boundary of a closed 2D polygon."""
    return min(
        _point_segment_distance(
            point,
            polygon[i],
            polygon[(i + 1) % len(polygon)],
        )
        for i in range(len(polygon))
    )


def _point_in_polygon(point, polygon):
    """Test containment using an odd-even horizontal ray."""
    inside = False
    previous = polygon[-1]

    for current in polygon:
        if (current.y > point.y) != (previous.y > point.y):
            x_crossing = (
                (previous.x - current.x)
                * (point.y - current.y)
                / (previous.y - current.y)
                + current.x
            )

            if point.x < x_crossing:
                inside = not inside

        previous = current

    return inside


# ---------------------------------------------------------------------------
# Preview geometry
# ---------------------------------------------------------------------------

def _extract_sections(
    mesh,
    matrix_world,
    plane_point,
    plane_normal,
    tolerance,
    keep_bmesh=False,
):
    """Bisect a world-space BMesh and extract closed section loops.

    No scene object or mesh datablock is modified.

    Edges are accepted only when adjacent faces extend to both plane sides.
    This excludes unrelated pre-existing coplanar face interiors.

    When keep_bmesh is True, ownership of the BMesh and its section edge
    references passes to the caller. Otherwise, the temporary BMesh is freed.
    """
    bm = bmesh.new()
    transferred = False

    try:
        bm.from_mesh(mesh)
        bm.transform(matrix_world)

        bmesh.ops.bisect_plane(
            bm,
            geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
            dist=tolerance,
            plane_co=plane_point,
            plane_no=plane_normal,
            use_snap_center=False,
            clear_inner=False,
            clear_outer=False,
        )

        candidates = []
        edge_tolerance = tolerance * 2.0

        for edge in bm.edges:
            if len(edge.link_faces) != 2:
                continue

            if any(
                abs(
                    (vertex.co - plane_point).dot(plane_normal)
                ) > edge_tolerance
                for vertex in edge.verts
            ):
                continue

            has_positive = False
            has_negative = False

            for face in edge.link_faces:
                for vertex in face.verts:
                    distance = (
                        vertex.co - plane_point
                    ).dot(plane_normal)
                    has_positive |= distance > tolerance
                    has_negative |= distance < -tolerance

            if has_positive and has_negative:
                candidates.append(edge)

        adjacency = {}
        for edge in candidates:
            for vertex in edge.verts:
                adjacency.setdefault(vertex, []).append(edge)

        remaining = set(candidates)
        loops = []
        loop_edges = []
        invalid_segments = []
        invalid_count = 0

        while remaining:
            seed = remaining.pop()
            component_edges = {seed}
            component_vertices = set(seed.verts)
            stack = list(seed.verts)

            while stack:
                vertex = stack.pop()

                for edge in adjacency.get(vertex, ()):
                    if edge not in component_edges:
                        component_edges.add(edge)
                        remaining.discard(edge)

                        other = edge.other_vert(vertex)
                        if other not in component_vertices:
                            component_vertices.add(other)
                            stack.append(other)

            valid = (
                len(component_vertices) >= 3
                and all(
                    len(adjacency[vertex]) == 2
                    for vertex in component_vertices
                )
            )

            if not valid:
                invalid_count += 1
                for edge in component_edges:
                    invalid_segments.extend((
                        edge.verts[0].co.copy(),
                        edge.verts[1].co.copy(),
                    ))
                continue

            start = seed.verts[0]
            vertex = start
            previous_edge = None
            ordered = []
            ordered_edges = []

            for _ in range(len(component_edges)):
                ordered.append(vertex.co.copy())

                edge = next(
                    edge
                    for edge in adjacency[vertex]
                    if edge is not previous_edge
                )

                ordered_edges.append(edge)
                vertex = edge.other_vert(vertex)
                previous_edge = edge

            if (
                vertex is start
                and len(ordered) == len(component_vertices)
            ):
                loops.append(ordered)
                loop_edges.append(ordered_edges)
            else:
                invalid_count += 1
                for edge in component_edges:
                    invalid_segments.extend((
                        edge.verts[0].co.copy(),
                        edge.verts[1].co.copy(),
                    ))

        if keep_bmesh:
            # Transfer ownership only after successful extraction.
            transferred = True
            return (
                loops,
                invalid_segments,
                invalid_count,
                bm,
                loop_edges,
            )

        return loops, invalid_segments, invalid_count

    finally:
        if not transferred:
            bm.free()


# ---------------------------------------------------------------------------
# Local separation and conservative caps
# ---------------------------------------------------------------------------

def _face_components(bm, blocked_edges=()):
    """Find face islands without crossing the specified section edges."""
    blocked = set(blocked_edges)
    remaining = set(bm.faces)
    components = []

    while remaining:
        seed = remaining.pop()
        component = {seed}
        stack = [seed]

        while stack:
            face = stack.pop()

            for edge in face.edges:
                if edge in blocked:
                    continue

                for neighbor in edge.link_faces:
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)

        components.append(component)

    return components


def _boundary_cycles(edges):
    """Order simple boundary cycles and reject open or branched boundaries."""
    adjacency = {}

    for edge in edges:
        for vertex in edge.verts:
            adjacency.setdefault(vertex, []).append(edge)

    if any(
        len(linked) != 2
        for linked in adjacency.values()
    ):
        raise ValueError(
            "The new cut boundary is open or branched."
        )

    remaining = set(edges)
    cycles = []

    while remaining:
        seed = next(iter(remaining))
        start = seed.verts[0]
        vertex = start
        previous = None
        vertices = []
        cycle_edges = []

        while True:
            vertices.append(vertex)

            edge = next(
                candidate
                for candidate in adjacency[vertex]
                if candidate is not previous
            )

            if edge not in remaining:
                raise ValueError(
                    "The cut boundary could not be ordered."
                )

            remaining.remove(edge)
            cycle_edges.append(edge)
            vertex = edge.other_vert(vertex)
            previous = edge

            if vertex is start:
                break

        if len(vertices) < 3:
            raise ValueError(
                "A cut boundary has fewer than three vertices."
            )

        cycles.append((vertices, cycle_edges))

    return cycles


def _signed_polygon_area(polygon):
    """Return the signed area of a closed 2D polygon."""
    return 0.5 * sum(
        polygon[index].x * polygon[(index + 1) % len(polygon)].y
        - polygon[(index + 1) % len(polygon)].x * polygon[index].y
        for index in range(len(polygon))
    )


def _segments_touch(a, b, c, d, epsilon):
    """Detect crossing or nearly touching planar segments."""
    if (
        max(a.x, b.x) < min(c.x, d.x) - epsilon
        or max(c.x, d.x) < min(a.x, b.x) - epsilon
        or max(a.y, b.y) < min(c.y, d.y) - epsilon
        or max(c.y, d.y) < min(a.y, b.y) - epsilon
    ):
        return False

    if min(
        _point_segment_distance(a, c, d),
        _point_segment_distance(b, c, d),
        _point_segment_distance(c, a, b),
        _point_segment_distance(d, a, b),
    ) <= epsilon:
        return True

    def cross(first, second):
        return first.x * second.y - first.y * second.x

    ab = b - a
    cd = d - c
    return (
        cross(ab, c - a) * cross(ab, d - a) < 0.0
        and cross(cd, a - c) * cross(cd, b - c) < 0.0
    )


def _section_groups(loops, plane_point, plane_normal, epsilon):
    """Group simple planar contours into material regions and their holes."""
    u, v = _plane_basis(plane_normal)
    polygons = [
        [
            Vector((
                (point - plane_point).dot(u),
                (point - plane_point).dot(v),
            ))
            for point in loop
        ]
        for loop in loops
    ]

    areas = []

    for polygon in polygons:
        count = len(polygon)
        if count < 3:
            raise ValueError("A section contour has fewer than three vertices.")

        area = abs(_signed_polygon_area(polygon))
        if area <= epsilon * epsilon:
            raise ValueError("A section contour has a degenerate area.")
        areas.append(area)

        for index in range(count):
            a = polygon[index]
            b = polygon[(index + 1) % count]

            if (b - a).length <= epsilon:
                raise ValueError(
                    "A section contour contains an extremely short edge."
                )

            # Adjacent edges share an endpoint and must not double back.
            previous = polygon[(index - 1) % count]
            if (
                _point_segment_distance(previous, a, b) <= epsilon
                or _point_segment_distance(b, previous, a) <= epsilon
            ):
                raise ValueError(
                    "A section contour contains overlapping adjacent edges."
                )

            for other in range(index + 1, count):
                if (
                    other == index + 1
                    or (index == 0 and other == count - 1)
                ):
                    continue

                c = polygon[other]
                d = polygon[(other + 1) % count]

                if _segments_touch(a, b, c, d, epsilon):
                    raise ValueError(
                        "A section contour intersects or touches itself."
                    )

    # Distinct contours must have an unambiguous nesting relationship.
    for first in range(len(polygons)):
        polygon = polygons[first]

        for second in range(first + 1, len(polygons)):
            other = polygons[second]

            for index, a in enumerate(polygon):
                b = polygon[(index + 1) % len(polygon)]

                for other_index, c in enumerate(other):
                    d = other[(other_index + 1) % len(other)]

                    if _segments_touch(a, b, c, d, epsilon):
                        raise ValueError(
                            "Section contours intersect or touch. "
                            "Move the cutting stroke slightly."
                        )

    parents = []

    for index, polygon in enumerate(polygons):
        containers = [
            other
            for other, candidate in enumerate(polygons)
            if other != index
            and areas[other] > areas[index]
            and _point_in_polygon(polygon[0], candidate)
        ]

        parents.append(
            min(containers, key=lambda other: areas[other])
            if containers
            else None
        )

    depths = []

    for index in range(len(polygons)):
        depth = 0
        parent = parents[index]

        while parent is not None:
            depth += 1
            if depth > len(polygons):
                raise ValueError("Section nesting contains a cycle.")
            parent = parents[parent]

        depths.append(depth)

    groups = []

    for index, depth in enumerate(depths):
        if depth % 2:
            continue

        holes = [
            other
            for other, parent in enumerate(parents)
            if parent == index
        ]

        expected_area = areas[index] - sum(
            areas[other] for other in holes
        )

        if expected_area <= epsilon * epsilon:
            raise ValueError("A section material region has no usable area.")

        groups.append({
            "outer": index,
            "holes": tuple(holes),
            "indices": (index, *holes),
            "expected_area": expected_area,
        })

    return polygons, groups


def _expand_section_selection(selected, groups):
    """Select every boundary belonging to a touched material region."""
    expanded = set()

    for group in groups:
        if selected.intersection(group["indices"]):
            expanded.update(group["indices"])

    return expanded


def _edge_side_faces(edge, plane_point, plane_normal, epsilon):
    """Return the negative and positive adjacent faces of a section edge."""
    sides = {}

    if len(edge.link_faces) != 2:
        raise ValueError("A selected section edge is not manifold.")

    for face in edge.link_faces:
        distances = [
            (vertex.co - plane_point).dot(plane_normal)
            for vertex in face.verts
        ]

        positive = max(distances) > epsilon
        negative = min(distances) < -epsilon

        if positive == negative:
            raise ValueError(
                "A section face cannot be assigned to one plane side."
            )

        side = 1 if positive else -1

        if side in sides:
            raise ValueError(
                "The adjacent section faces are not on opposite plane sides."
            )

        sides[side] = face

    return sides


def _section_winding(loop, edges, positive_face, polygon, epsilon):
    """Get the directed contour winding from the positive-side wall face."""
    edge = edges[0]
    face_loop = next(
        face_loop
        for face_loop in positive_face.loops
        if face_loop.edge == edge
    )

    # Extracted contours and their edge lists use the same traversal order.
    same_direction = (
        face_loop.vert.co - loop[0]
    ).length <= epsilon

    signed_area = _signed_polygon_area(polygon)
    return signed_area if same_direction else -signed_area


def _section_partitions(operator):
    """Join wall components through selected ring caps on each plane side."""
    bm = operator._cut_bm
    point = operator._plane_point
    normal = operator._plane_normal
    epsilon = operator._cut_tolerance * 2.0

    polygons, groups = _section_groups(
        operator._cut_loops,
        point,
        normal,
        epsilon,
    )

    selected_groups = [
        group
        for group in groups
        if operator._cut_selected.intersection(group["indices"])
    ]

    for group in selected_groups:
        if not set(group["indices"]).issubset(operator._cut_selected):
            raise ValueError(
                "The selected material region is incomplete. Redraw the preview."
            )

    selected_edges = {
        edge
        for group in selected_groups
        for index in group["indices"]
        for edge in operator._cut_loop_edges[index]
    }

    components = _face_components(bm, selected_edges)
    component_of = {
        face: index
        for index, component in enumerate(components)
        for face in component
    }

    source_components = _face_components(bm)
    source_component_of = {
        face: index
        for index, component in enumerate(source_components)
        for face in component
    }

    parents = list(range(len(components)))
    source_parents = list(range(len(source_components)))

    def find(table, item):
        while table[item] != item:
            table[item] = table[table[item]]
            item = table[item]
        return item

    def join(table, items):
        items = list(items)
        if not items:
            return

        root = find(table, items[0])
        for item in items[1:]:
            table[find(table, item)] = root

    side_records = []

    for group in selected_groups:
        side_components = {-1: set(), 1: set()}
        shell_components = set()
        windings = {}

        for index in group["indices"]:
            loop_edges = operator._cut_loop_edges[index]
            loop_sides = {-1: set(), 1: set()}
            positive_face = None

            for edge in loop_edges:
                sides = _edge_side_faces(
                    edge, point, normal, epsilon,
                )

                for side, face in sides.items():
                    loop_sides[side].add(component_of[face])
                    shell_components.add(source_component_of[face])

                if positive_face is None:
                    positive_face = sides[1]

            if any(len(items) != 1 for items in loop_sides.values()):
                raise ValueError(
                    "A section loop does not have a unique component on each side."
                )

            if loop_sides[-1] == loop_sides[1]:
                raise ValueError(
                    "A selected section loop does not separate the surface."
                )

            for side in (-1, 1):
                side_components[side].update(loop_sides[side])

            windings[index] = _section_winding(
                operator._cut_loops[index],
                loop_edges,
                positive_face,
                polygons[index],
                epsilon,
            )

        # Nested solid shells must not be mistaken for cavity walls.
        outer_winding = windings[group["outer"]]

        for hole in group["holes"]:
            if outer_winding * windings[hole] >= 0.0:
                raise ValueError(
                    "Outer and inner wall orientations are inconsistent. "
                    "Check the source mesh normals."
                )

        for side in (-1, 1):
            join(parents, side_components[side])

        # A cavity shell may be disconnected before caps are created.
        join(source_parents, shell_components)
        side_records.append(side_components)

    # Do not silently distribute unrelated solids or untouched cavity shells.
    if len({
        find(source_parents, index)
        for index in range(len(source_components))
    }) != 1:
        raise ValueError(
            "The source contains unrelated or uncut separate surface shells. "
            "This B3 version cannot safely assign them to result parts."
        )

    for record in side_records:
        negative = {
            find(parents, index)
            for index in record[-1]
        }
        positive = {
            find(parents, index)
            for index in record[1]
        }

        if negative.intersection(positive):
            raise ValueError(
                "The selected material regions do not produce a valid separation."
            )

    partitions = {}

    for index, component in enumerate(components):
        root = find(parents, index)
        partitions.setdefault(root, set()).update(component)

    if len(partitions) < 2:
        raise ValueError(
            "The selected regions do not separate the mesh into distinct parts."
        )

    return list(partitions.values())


def _fill_section_caps(bm, plane_point, plane_normal, tolerance):
    """Fill new boundaries as planar material regions, preserving holes."""
    epsilon = tolerance * 2.0
    boundaries = [
        edge for edge in bm.edges if edge.is_boundary
    ]

    if not boundaries:
        raise ValueError("A result part has no expected cut boundary.")

    cycles = _boundary_cycles(boundaries)
    loops = [
        [vertex.co.copy() for vertex in vertices]
        for vertices, _edges in cycles
    ]

    if any(
        abs((point - plane_point).dot(plane_normal)) > tolerance * 8.0
        for loop in loops
        for point in loop
    ):
        raise ValueError("A new boundary is not on the stored cutting plane.")

    polygons, groups = _section_groups(
        loops, plane_point, plane_normal, epsilon,
    )
    u, v = _plane_basis(plane_normal)

    for group in groups:
        edges = [
            edge
            for index in group["indices"]
            for edge in cycles[index][1]
        ]
        faces_before = set(bm.faces)

        # Use the same ring-aware operation as the existing planar cap path.
        # Any failure aborts the entire disposable result BMesh.
        bmesh.ops.triangle_fill(
            bm,
            edges=edges,
            use_beauty=True,
            use_dissolve=False,
            normal=plane_normal,
        )

        caps = [
            face for face in bm.faces
            if face not in faces_before
        ]

        if not caps or any(len(face.verts) != 3 for face in caps):
            raise ValueError("A material region could not be triangulated.")

        outer = polygons[group["outer"]]
        holes = [
            polygons[index] for index in group["holes"]
        ]

        def belongs_to_material(point):
            if _polygon_distance(point, outer) <= epsilon:
                inside_outer = True
            else:
                inside_outer = _point_in_polygon(point, outer)

            if not inside_outer:
                return False

            return not any(
                _point_in_polygon(point, hole)
                and _polygon_distance(point, hole) > epsilon
                for hole in holes
            )

        for face in caps:
            projected = [
                Vector((
                    (vertex.co - plane_point).dot(u),
                    (vertex.co - plane_point).dot(v),
                ))
                for vertex in face.verts
            ]

            if abs(_signed_polygon_area(projected)) <= epsilon * epsilon:
                raise ValueError("The cap contains a degenerate triangle.")

            center = sum(
                projected, Vector((0.0, 0.0)),
            ) / len(projected)

            samples = [center] + [
                (projected[index] + projected[(index + 1) % 3]) * 0.5
                for index in range(3)
            ]

            if not all(belongs_to_material(point) for point in samples):
                raise ValueError(
                    "The generated cap covers a hole or leaves the material region."
                )

            face.smooth = False

        actual_area = sum(face.calc_area() for face in caps)
        expected_area = group["expected_area"]
        allowed_error = max(
            expected_area * 1e-5,
            epsilon * epsilon * 16.0,
        )

        if abs(actual_area - expected_area) > allowed_error:
            raise ValueError(
                "The generated cap area does not match the material region."
            )

        cap_set = set(caps)

        # Every original boundary must now meet exactly one cap face.
        for edge in edges:
            if (
                len(edge.link_faces) != 2
                or sum(face in cap_set for face in edge.link_faces) != 1
            ):
                raise ValueError(
                    "A cap did not correctly connect to its wall boundary."
                )

        # New internal triangulation edges must meet two cap faces.
        internal_edges = {
            edge
            for face in caps
            for edge in face.edges
            if edge not in set(edges)
        }

        if any(
            len(edge.link_faces) != 2
            or any(face not in cap_set for face in edge.link_faces)
            for edge in internal_edges
        ):
            raise ValueError("The cap has an invalid internal triangulation.")

    if any(len(edge.link_faces) != 2 for edge in bm.edges):
        raise ValueError("A result part has open or non-manifold edges.")

    # Ring caps must connect inner and outer walls into one result surface.
    if len(_face_components(bm)) != 1:
        raise ValueError(
            "The capped result still contains disconnected surface shells."
        )


def _prepare_freehand_seam_regions(operator, component_indices):
    """Associate each selected material region with its sorted result parts."""
    bm = operator._cut_bm
    point = operator._plane_point
    normal = operator._plane_normal
    epsilon = operator._cut_tolerance * 2.0

    face_to_part = {
        face_index: part_index
        for part_index, indices in enumerate(component_indices)
        for face_index in indices
    }

    if len(face_to_part) != len(bm.faces):
        raise ValueError(
            "The Freehand partitions do not cover every source face."
        )

    _polygons, groups = _section_groups(
        operator._cut_loops,
        point,
        normal,
        epsilon,
    )

    regions = []

    for group in groups:
        if not operator._cut_selected.intersection(group["indices"]):
            continue

        if not set(group["indices"]).issubset(operator._cut_selected):
            raise ValueError("A selected seam region is incomplete.")

        partners = {-1: set(), 1: set()}

        for loop_index in group["indices"]:
            for edge in operator._cut_loop_edges[loop_index]:
                sides = _edge_side_faces(
                    edge,
                    point,
                    normal,
                    epsilon,
                )

                for side, face in sides.items():
                    partners[side].add(face_to_part[face.index])

        if any(len(indices) != 1 for indices in partners.values()):
            raise ValueError(
                "A material region has ambiguous result partners."
            )

        negative = next(iter(partners[-1]))
        positive = next(iter(partners[1]))

        if negative == positive:
            raise ValueError(
                "Both sides of a seam belong to the same result part."
            )

        regions.append({
            "negative_part": negative,
            "positive_part": positive,
            "outer": [
                point.copy()
                for point in operator._cut_loops[group["outer"]]
            ],
            "holes": [
                [
                    point.copy()
                    for point in operator._cut_loops[loop_index]
                ]
                for loop_index in group["holes"]
            ],
        })

    if not regions:
        raise ValueError("No selected Freehand seam regions were found.")

    return regions



def _build_freehand_meshes(operator, cap_seams):
    """Build parts and optionally close their selected material regions."""

    bm = operator._cut_bm
    source = operator._mesh

    if bm is None or not operator._cut_selected:
        raise ValueError("No valid cutting preview is available.")

    if getattr(operator, "_cut_invalid_count", 0):
        raise ValueError(
            "The preview contains open or branched sections. "
            "Move the cutting stroke and try again."
        )

    # Open-ended tubes with a complete wall rim are manifold surfaces.
    # Actual missing wall faces or uncapped wall thickness remain unsupported.
    if any(len(edge.link_faces) != 2 for edge in bm.edges):
        raise ValueError(
            "Freehand B3 requires a closed manifold material surface."
        )

    if any(not vertex.link_faces for vertex in bm.verts):
        raise ValueError("Loose vertices are not supported.")

    components = _section_partitions(operator)

    bm.faces.index_update()
    component_indices = [
        {face.index for face in component}
        for component in components
    ]
    component_indices.sort(key=len, reverse=True)

    # Bind seams to the exact order used for mesh creation and publication.
    seam_regions = _prepare_freehand_seam_regions(
        operator,
        component_indices,
    )

    inverse = operator._matrix_world.inverted()

    meshes = []

    try:
        for number, indices in enumerate(component_indices, start=1):
            part_bm = bm.copy()

            try:
                part_bm.faces.ensure_lookup_table()
                remove_faces = [
                    face
                    for index, face in enumerate(part_bm.faces)
                    if index not in indices
                ]

                bmesh.ops.delete(
                    part_bm,
                    geom=remove_faces,
                    context='FACES_ONLY',
                )

                unused_vertices = [
                    vertex for vertex in part_bm.verts
                    if not vertex.link_faces
                ]
                if unused_vertices:
                    bmesh.ops.delete(
                        part_bm,
                        geom=unused_vertices,
                        context='VERTS',
                    )

                unused_edges = [
                    edge for edge in part_bm.edges
                    if not edge.link_faces
                ]
                if unused_edges:
                    bmesh.ops.delete(
                        part_bm,
                        geom=unused_edges,
                        context='EDGES',
                    )

                # Preserve open cut boundaries when automatic capping is disabled.
                if cap_seams:
                    _fill_section_caps(
                        part_bm,
                        operator._plane_point,
                        operator._plane_normal,
                        operator._cut_tolerance,
                    )


                part_bm.transform(inverse)
                bmesh.ops.recalc_face_normals(
                    part_bm,
                    faces=list(part_bm.faces),
                )

                mesh = source.copy()
                meshes.append(mesh)
                mesh.name = (
                    f"{operator._obj.name}_Freehand_{number:02d}"
                )

                part_bm.to_mesh(mesh)
                mesh.update()

            finally:
                part_bm.free()

        return meshes, seam_regions


    except Exception:
        for mesh in meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        raise



# ---------------------------------------------------------------------------
# Transactional scene publication
# ---------------------------------------------------------------------------

def _publish_freehand_parts(
    context,
    operator,
    meshes,
    seam_regions,
    cap_seams,
):
    """Publish prepared parts and hide the unchanged source only on success."""
    source = operator._obj
    selected_before = list(context.selected_objects)
    active_before = context.view_layer.objects.active
    hidden_before = source.hide_get()
    render_before = source.hide_render

    root = bpy.data.collections.get(PARTS_COLLECTION_NAME)
    root_created = False
    root_linked = False
    job = None
    objects = []
    rollback_seams = None

    try:
        if root is None:
            root = bpy.data.collections.new(
                PARTS_COLLECTION_NAME
            )
            root_created = True

        if not any(
            child == root
            for child in context.scene.collection.children
        ):
            context.scene.collection.children.link(root)
            root_linked = True

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job = bpy.data.collections.new(
            f"{source.name}_Freehand_{stamp}"
        )
        root.children.link(job)

        for number, mesh in enumerate(meshes, start=1):
            obj = bpy.data.objects.new(
                f"{source.name}_Freehand_{number:02d}",
                mesh,
            )
            objects.append(obj)

            obj.matrix_world = operator._matrix_world.copy()
            obj.color = source.color[:]
            job.objects.link(obj)

        # Keep metadata creation inside the existing publication transaction.
        tangent, _bitangent = _plane_basis(operator._plane_normal)

        write_freehand_seams(
            objects=objects,
            regions=seam_regions,
            plane_point=operator._plane_point,
            plane_normal=operator._plane_normal,
            tangent=tangent,
            capped=cap_seams,
            tolerance=operator._cut_tolerance,
        )

        # Transfer old seams only after all new result identities exist.
        rollback_seams = migrate_intact_freehand_seams(
            source,
            objects,
        )


        context.view_layer.update()


        # Never hide the source when results are excluded or invisible.
        if any(
            not obj.visible_get()
            for obj in objects
        ):
            raise ValueError(
                "The Parts collection is hidden or excluded. "
                "Make it visible and retry."
            )

        for obj in list(context.selected_objects):
            obj.select_set(False)

        for obj in objects:
            obj.select_set(True)

        context.view_layer.objects.active = objects[0]

        # Hide the original only after every result has been published.
        source.hide_set(True)
        source.hide_render = True

        return objects

    except Exception:
        # Restore metadata while all referenced objects still exist.
        if rollback_seams is not None:
            rollback_seams()

        # Remove newly published objects only after metadata restoration.
        for obj in objects:
            bpy.data.objects.remove(
                obj,
                do_unlink=True,
            )

        if job is not None:
            bpy.data.collections.remove(job)


        if root_created:
            bpy.data.collections.remove(root)
        elif root_linked:
            context.scene.collection.children.unlink(root)

        for mesh in meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        source.hide_set(hidden_before)
        source.hide_render = render_before

        for obj in selected_before:
            obj.select_set(True)

        context.view_layer.objects.active = active_before
        raise


# ---------------------------------------------------------------------------
# Modal operator
# ---------------------------------------------------------------------------

class SNAP_OT_freehand_cut(Operator):
    """Preview and execute a local planar cut from a freehand stroke."""

    bl_idname = "snapsplit.freehand_cut"
    bl_label = "Freehand Cut"
    bl_description = (
        "Draw a local planar cut and preview touched material regions. "
        "Press Enter to split; Cap seams during split controls closure"
    )

    bl_options = {'REGISTER', 'UNDO'}

    brush_radius_px: FloatProperty(
        name="Brush Radius",
        description=(
            "Screen-space tolerance for touching a section loop"
        ),
        default=DEFAULT_BRUSH_RADIUS,
        min=1.0,
        max=100.0,
        options={'SKIP_SAVE'},
    )

    @classmethod
    def poll(cls, context):
        """Require a 3D viewport and an active mesh in Object Mode."""
        obj = context.active_object

        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.mode == 'OBJECT'
            and obj is not None
            and obj.type == 'MESH'
        )

    def invoke(self, context, event):
        """Start previewing and install viewport-scoped draw handlers."""
        if _ACTIVE_OPERATORS:
            report_user(
                self,
                'WARNING',
                "A Freehand Cut preview is already active.",
            )
            return {'CANCELLED'}

        obj = context.active_object

        if obj.modifiers:
            report_user(
                self,
                'ERROR',
                "Freehand Cut requires an object without modifiers. "
                "Apply or remove the modifiers first.",
            )
            return {'CANCELLED'}

        if obj.data.shape_keys is not None:
            report_user(
                self,
                'ERROR',
                "Freehand Cut does not support shape keys.",
            )
            return {'CANCELLED'}

        if not obj.data.polygons:
            report_user(
                self,
                'ERROR',
                "The active mesh has no faces.",
            )
            return {'CANCELLED'}

        if context.space_data.region_quadviews:
            report_user(
                self,
                'ERROR',
                "Please leave Quad View before starting Freehand Cut.",
            )
            return {'CANCELLED'}

        region = next(
            (
                region
                for region in context.area.regions
                if region.type == 'WINDOW'
            ),
            None,
        )

        if region is None:
            report_user(
                self,
                'ERROR',
                "No viewport window region was found.",
            )
            return {'CANCELLED'}

        try:
            obj.matrix_world.inverted()
        except ValueError:
            report_user(
                self,
                'ERROR',
                "The object transform is singular.",
            )
            return {'CANCELLED'}

        self._obj = obj
        self._mesh = obj.data
        self._matrix_world = obj.matrix_world.copy()
        self._mesh_counts = self._counts()
        self._geometry_signature = _geometry_signature(
            self._mesh
        )

        self._cut_bm = None
        self._cut_loops = []
        self._cut_loop_edges = []
        self._cut_selected = set()
        self._cut_tolerance = None
        self._cut_invalid_count = 0

        self._area = context.area
        self._region = region
        self._rv3d = context.space_data.region_3d
        self._window = context.window
        self._wm = context.window_manager

        self._handle_pixel = None
        self._handle_view = None
        self._timer = None
        self._closed = False
        self._drawing = False
        self._points = []
        self._stroke_batch = None
        self._preview_batches = []
        self._plane_point = None
        self._plane_normal = None
        self._selected_count = 0
        self._draw_error = None

        try:
            self._shader = gpu.shader.from_builtin(
                'POLYLINE_UNIFORM_COLOR'
            )
            self._polyline_shader = True

        except Exception:
            try:
                self._shader = gpu.shader.from_builtin(
                    'UNIFORM_COLOR'
                )
                self._polyline_shader = False

            except Exception as exc:
                self._cleanup()
                report_user(
                    self,
                    'ERROR',
                    "Cannot create preview shader: {error}",
                    error=exc,
                )
                return {'CANCELLED'}

        try:
            self._handle_pixel = (
                bpy.types.SpaceView3D.draw_handler_add(
                    self._draw_pixel,
                    (),
                    'WINDOW',
                    'POST_PIXEL',
                )
            )
            self._handle_view = (
                bpy.types.SpaceView3D.draw_handler_add(
                    self._draw_view,
                    (),
                    'WINDOW',
                    'POST_VIEW',
                )
            )
            self._timer = self._wm.event_timer_add(
                0.25,
                window=self._window,
            )

            _ACTIVE_OPERATORS.append(self)
            self._wm.modal_handler_add(self)

            self._set_header(
                "Draw with LMB | Shift-release: axis snap | Esc/RMB: exit"
            )

        except Exception as exc:
            self._cleanup()
            report_user(
                self,
                'ERROR',
                "Cannot start preview: {error}",
                error=exc,
            )
            return {'CANCELLED'}

        warn_if_unapplied_transforms(
            obj,
            operator=self,
        )
        self._area.tag_redraw()
        return {'RUNNING_MODAL'}

    def _clear_cut_data(self):
        """Free retained preview geometry and reset the cutting payload."""
        bm = getattr(self, "_cut_bm", None)

        # Clear the reference before releasing the owned resource.
        self._cut_bm = None
        self._cut_loops = []
        self._cut_loop_edges = []
        self._cut_selected = set()
        self._cut_tolerance = None
        self._cut_invalid_count = 0


        if bm is not None:
            bm.free()

    def _commit_cut(self, context):
        """Validate the source and publish only completely prepared results."""
        if not self._source_valid(context):
            raise ValueError(
                "The source object changed. Start Freehand Cut again."
            )

        if (
            _geometry_signature(self._mesh)
            != self._geometry_signature
        ):
            raise ValueError(
                "Source coordinates or topology changed. "
                "Start Freehand Cut again."
            )

        if self._mesh.shape_keys is not None:
            raise ValueError(
                "Shape keys are not supported."
            )
        # Archived backups must not become active seam owners accidentally.
        if "snapsplit_seam_archive" in self._obj:
            raise ValueError(
                "This object is an archived cut source. "
                "Use an active Freehand result or undo the previous cut."
            )

        # Legacy metadata needs its own migration path.
        if any(
            str(key).startswith("snapsplit_seam")
            and str(key) not in {
                "snapsplit_seam_data",
                "snapsplit_seam_object_id",
            }
            for key in self._obj.keys()
        ):
            raise ValueError(
                "The source contains unsupported legacy seam metadata."
            )


        # Result objects do not inherit rigging, animation or constraints.
        if (
            self._obj.vertex_groups
            or self._obj.constraints
            or self._obj.animation_data is not None
            or self._mesh.animation_data is not None
        ):
            raise ValueError(
                "This cutting version does not support vertex groups, "
                "constraints or animation."
            )

        # Read the shared split setting when the user confirms the cut.
        cap_seams = bool(
            context.scene.snapsplit.cap_seams_during_split
        )

        meshes, seam_regions = _build_freehand_meshes(
            self,
            cap_seams,
        )

        objects = _publish_freehand_parts(
            context,
            self,
            meshes,
            seam_regions,
            cap_seams,
        )

        return len(objects), cap_seams



    def _counts(self):
        """Return a cheap topology signature for the original mesh."""
        return (
            len(self._mesh.vertices),
            len(self._mesh.edges),
            len(self._mesh.polygons),
        )

    def _source_valid(self, context):
        """Reject obvious source changes rather than showing stale geometry."""
        try:
            return (
                context.mode == 'OBJECT'
                and context.active_object == self._obj
                and self._obj.data == self._mesh
                and not self._obj.modifiers
                and self._counts() == self._mesh_counts
                and self._obj.matrix_world == self._matrix_world
            )
        except ReferenceError:
            return False

    def _mouse(self, event):
        """Convert window coordinates to the originating WINDOW region."""
        return Vector((
            event.mouse_x - self._region.x,
            event.mouse_y - self._region.y,
        ))

    def _inside(self, point):
        """Test whether a mouse position lies inside the viewport."""
        return (
            0 <= point.x < self._region.width
            and 0 <= point.y < self._region.height
        )

    def _ray(self, coordinate):
        """Build a world-space ray from the current viewport."""
        origin = view3d_utils.region_2d_to_origin_3d(
            self._region,
            self._rv3d,
            coordinate,
        )
        direction = (
            view3d_utils.region_2d_to_vector_3d(
                self._region,
                self._rv3d,
                coordinate,
            ).normalized()
        )
        return origin, direction

    def _hit(self, coordinate):
        """Raycast only the active object and return a world-space hit."""
        origin, direction = self._ray(coordinate)
        inverse = self._matrix_world.inverted()

        local_origin = inverse @ origin
        local_direction = inverse.to_3x3() @ direction

        if local_direction.length_squared <= 1e-20:
            return None

        result, location, _normal, _index = self._obj.ray_cast(
            local_origin,
            local_direction.normalized(),
        )

        return (
            self._matrix_world @ location
            if result
            else None
        )

    def _append_point(self, point, force=False):
        """Collect a bounded stroke while preserving its complete extent."""
        if (
            not self._points
            or force
            or (point - self._points[-1]).length >= 2.0
        ):
            if (
                self._points
                and (point - self._points[-1]).length < 1e-6
            ):
                return

            self._points.append(point.copy())

            if len(self._points) > MAX_STROKE_POINTS:
                self._points = (
                    self._points[::2]
                    + [self._points[-1]]
                )

            if len(self._points) >= 2:
                self._stroke_batch = batch_for_shader(
                    self._shader,
                    'LINE_STRIP',
                    {
                        "pos": [
                            (point.x, point.y, 0.0)
                            for point in self._points
                        ]
                    },
                )

    def _world_pixel_radius(self, coordinate, world_point):
        """Convert brush pixels to a world-space tolerance at the hit depth."""
        center = view3d_utils.region_2d_to_location_3d(
            self._region,
            self._rv3d,
            coordinate,
            world_point,
        )
        shifted = view3d_utils.region_2d_to_location_3d(
            self._region,
            self._rv3d,
            coordinate + Vector((self.brush_radius_px, 0.0)),
            world_point,
        )
        return (shifted - center).length

    def _build_preview(self, snap):
        """Fit the plane and retain the exact locally selected cut geometry."""
        self._clear_cut_data()
        self._preview_batches = []
        self._selected_count = 0
        self._plane_point = None
        self._plane_normal = None

        if (
            _geometry_signature(self._mesh)
            != self._geometry_signature
        ):
            raise ValueError(
                "Source coordinates or topology changed. "
                "Start Freehand Cut again."
            )

        samples = _resample_stroke(self._points)
        _center, endpoint_a, endpoint_b = _fit_line(samples)

        hits = []
        for coordinate in samples:
            location = self._hit(coordinate)
            if location is not None:
                hits.append((coordinate, location))

        if not hits:
            raise ValueError(
                "The stroke did not hit the active mesh."
            )

        origin_a, direction_a = self._ray(endpoint_a)
        origin_b, direction_b = self._ray(endpoint_b)

        if self._rv3d.is_perspective:
            normal = direction_a.cross(direction_b)
        else:
            normal = (
                origin_b - origin_a
            ).cross(direction_a)

        if normal.length_squared <= 1e-16:
            raise ValueError(
                "Cannot determine a stable cutting plane."
            )

        normal.normalize()

        # Anchor near the surface instead of using a distant camera origin.
        anchor = (
            sum(
                (hit for _, hit in hits),
                Vector((0.0, 0.0, 0.0)),
            )
            / len(hits)
        )
        plane_point = (
            anchor
            - normal * (anchor - origin_a).dot(normal)
        )

        if snap:
            axis = max(
                range(3),
                key=lambda index: abs(normal[index]),
            )
            sign = 1.0 if normal[axis] >= 0.0 else -1.0
            normal = Vector((0.0, 0.0, 0.0))
            normal[axis] = sign
            plane_point = anchor.copy()

        corners = [
            self._matrix_world @ Vector(corner)
            for corner in self._obj.bound_box
        ]
        low = Vector(tuple(
            min(point[i] for point in corners)
            for i in range(3)
        ))
        high = Vector(tuple(
            max(point[i] for point in corners)
            for i in range(3)
        ))
        diagonal = (high - low).length

        if diagonal <= 1e-12:
            raise ValueError(
                "The object is too small or degenerate."
            )

        tolerance = max(
            diagonal * 1e-7,
            1e-10,
        )

        # The retained BMesh uses this exact offset plane for the actual cut.
        plane_point += normal * (tolerance * 4.0)

        (
            loops,
            invalid_segments,
            invalid_count,
            self._cut_bm,
            loop_edges,
        ) = _extract_sections(
            self._mesh,
            self._matrix_world,
            plane_point,
            normal,
            tolerance,
            keep_bmesh=True,
        )

        u, v = _plane_basis(normal)
        polygons = [
            [
                Vector((
                    (point - plane_point).dot(u),
                    (point - plane_point).dot(v),
                ))
                for point in loop
            ]
            for loop in loops
        ]

        selected = set()

        for coordinate, hit in hits:
            projected = (
                hit
                - normal * (hit - plane_point).dot(normal)
            )
            point_2d = Vector((
                (projected - plane_point).dot(u),
                (projected - plane_point).dot(v),
            ))
            radius = max(
                self._world_pixel_radius(coordinate, hit),
                tolerance * 8.0,
            )

            eligible = []

            for index, polygon in enumerate(polygons):
                distance = _polygon_distance(
                    point_2d,
                    polygon,
                )

                if (
                    distance <= radius
                    or _point_in_polygon(point_2d, polygon)
                ):
                    eligible.append((distance, index))
            if eligible:
                # First identify the nearest touched boundary.
                selected.add(min(eligible)[1])

        # Expand touched boundaries to complete material regions.
        # Inner rims are visibly selected before Enter can cut them.
        _polygons, groups = _section_groups(
            loops,
            plane_point,
            normal,
            tolerance * 2.0,
        )
        selected = _expand_section_selection(selected, groups)
        self._cut_invalid_count = invalid_count

        selected_region_count = sum(
            bool(selected.intersection(group["indices"]))
            for group in groups
        )

        for index, loop in enumerate(loops):

            coordinates = []

            for i, point in enumerate(loop):
                coordinates.extend((
                    point,
                    loop[(i + 1) % len(loop)],
                ))

            batch = batch_for_shader(
                self._shader,
                'LINES',
                {"pos": coordinates},
            )
            self._preview_batches.append((
                batch,
                ORANGE if index in selected else GRAY,
                3.0 if index in selected else 1.5,
            ))

        if invalid_segments:
            batch = batch_for_shader(
                self._shader,
                'LINES',
                {"pos": invalid_segments},
            )
            self._preview_batches.append((
                batch,
                INVALID_COLOR,
                2.0,
            ))

        self._plane_point = plane_point.copy()
        self._plane_normal = normal.copy()
        self._selected_count = len(selected)

        self._cut_loops = loops
        self._cut_loop_edges = loop_edges
        self._cut_selected = set(selected)
        self._cut_tolerance = tolerance

        self._set_header(
            f"Preview: {selected_region_count}/{len(groups)} material regions"
            f" | {len(selected)} boundary loops selected"
            " | Enter: cut | LMB: redraw | MMB: orbit | Esc: exit"
        )

        report_user(
            self,
            'INFO',
            "Preview: {selected} of {total} material regions selected "
            "with {loops} boundary loops. No mesh was changed.",
            selected=selected_region_count,
            total=len(groups),
            loops=len(selected),
        )


        if invalid_count:
            report_user(
                self,
                'WARNING',
                "{count} open or branched section(s) "
                "were excluded and shown in red.",
                count=invalid_count,
            )

        if not selected:
            report_user(
                self,
                'WARNING',
                "No valid section loop was touched. "
                "Try a straighter stroke.",
            )

    # -----------------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------------

    def _draw_here(self):
        """Restrict shared SpaceView3D handlers to the originating region."""
        context = bpy.context

        return (
            not self._closed
            and context.area == self._area
            and context.region == self._region
        )

    def _draw_batches(self, batches):
        """Draw cached batches and restore the previous GPU state."""
        old_blend = gpu.state.blend_get()
        old_depth = gpu.state.depth_test_get()
        old_mask = gpu.state.depth_mask_get()
        old_width = gpu.state.line_width_get()

        try:
            gpu.state.blend_set('ALPHA')
            gpu.state.depth_test_set('NONE')
            gpu.state.depth_mask_set(False)

            self._shader.bind()

            for batch, color, width in batches:
                self._shader.uniform_float(
                    "color",
                    color,
                )

                if self._polyline_shader:
                    self._shader.uniform_float(
                        "viewportSize",
                        gpu.state.viewport_get()[2:],
                    )
                    self._shader.uniform_float(
                        "lineWidth",
                        width,
                    )
                else:
                    gpu.state.line_width_set(1.0)

                batch.draw(self._shader)

        finally:
            gpu.state.line_width_set(old_width)
            gpu.state.depth_mask_set(old_mask)
            gpu.state.depth_test_set(old_depth)
            gpu.state.blend_set(old_blend)

    def _draw_pixel(self):
        """Draw the stroke in screen space only while dragging."""
        if (
            not self._draw_here()
            or not self._drawing
            or self._stroke_batch is None
        ):
            return

        try:
            self._draw_batches([
                (self._stroke_batch, ORANGE, 3.0)
            ])
        except Exception as exc:
            self._draw_error = str(exc)

    def _draw_view(self):
        """Draw section loops in world space, including hidden portions."""
        if (
            not self._draw_here()
            or self._drawing
            or not self._preview_batches
        ):
            return

        try:
            self._draw_batches(self._preview_batches)
        except Exception as exc:
            self._draw_error = str(exc)

    def _set_header(self, text):
        """Display modal instructions in the viewport header."""
        self._area.header_text_set(text)

    # -----------------------------------------------------------------------
    # Resource lifecycle
    # -----------------------------------------------------------------------

    def _cleanup(self):
        """Remove every owned resource; repeated calls are harmless."""
        if getattr(self, "_closed", True):
            return

        self._closed = True
        self._clear_cut_data()

        for attribute in (
            "_handle_pixel",
            "_handle_view",
        ):
            handle = getattr(self, attribute, None)

            if handle is not None:
                try:
                    bpy.types.SpaceView3D.draw_handler_remove(
                        handle,
                        'WINDOW',
                    )
                except (
                    ReferenceError,
                    ValueError,
                    RuntimeError,
                ):
                    pass

                setattr(self, attribute, None)

        if self._timer is not None:
            try:
                self._wm.event_timer_remove(self._timer)
            except (
                ReferenceError,
                ValueError,
                RuntimeError,
            ):
                pass

            self._timer = None

        try:
            self._area.header_text_set(None)
            self._area.tag_redraw()
        except ReferenceError:
            pass

        self._stroke_batch = None
        self._preview_batches = []

        if self in _ACTIVE_OPERATORS:
            _ACTIVE_OPERATORS.remove(self)

    def cancel(self, context):
        """Support Blender-driven cancellation as well as explicit exit."""
        self._cleanup()

    # -----------------------------------------------------------------------
    # Modal interaction
    # -----------------------------------------------------------------------

    def modal(self, context, event):
        """Handle drawing, cutting, navigation and safe cancellation."""
        if self._closed:
            return {'CANCELLED'}

        try:
            # Collection membership expects names, so compare Area objects.
            if not any(
                area == self._area
                for area in self._window.screen.areas
            ):
                self._cleanup()
                return {'CANCELLED'}

            if not self._source_valid(context):
                report_user(
                    self,
                    'WARNING',
                    "The active object changed. "
                    "Freehand Cut preview was cancelled.",
                )
                self._cleanup()
                return {'CANCELLED'}

            if self._draw_error is not None:
                report_user(
                    self,
                    'ERROR',
                    "Preview drawing failed: {error}",
                    error=self._draw_error,
                )
                self._cleanup()
                return {'CANCELLED'}

            if (
                event.type in {'ESC', 'RIGHTMOUSE'}
                and event.value == 'PRESS'
            ):
                self._cleanup()
                return {'CANCELLED'}

            if event.type == 'TIMER':
                return {'RUNNING_MODAL'}

            point = self._mouse(event)

            if (
                event.type == 'LEFTMOUSE'
                and event.value == 'PRESS'
            ):
                if not self._inside(point):
                    return {'RUNNING_MODAL'}

                # Preserve alternative Alt-LMB navigation layouts.
                if event.alt:
                    return {'PASS_THROUGH'}

                self._clear_cut_data()
                self._drawing = True
                self._points = []
                self._stroke_batch = None
                self._preview_batches = []
                self._selected_count = 0
                self._plane_point = None
                self._plane_normal = None

                self._append_point(point)
                self._set_header(
                    "Drawing | Release LMB to preview | Shift: axis snap"
                )
                self._area.tag_redraw()
                return {'RUNNING_MODAL'}

            if self._drawing:
                if event.type == 'MOUSEMOVE':
                    self._append_point(point)
                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                if (
                    event.type == 'LEFTMOUSE'
                    and event.value == 'RELEASE'
                ):
                    self._append_point(
                        point,
                        force=True,
                    )
                    self._drawing = False
                    self._stroke_batch = None

                    try:
                        self._build_preview(
                            snap=event.shift
                        )

                    except (ValueError, RuntimeError) as exc:
                        self._clear_cut_data()
                        self._preview_batches = []
                        self._selected_count = 0
                        self._plane_point = None
                        self._plane_normal = None

                        self._set_header(
                            "Draw again with LMB"
                            " | Shift-release: axis snap | Esc: exit"
                        )

                        report_user(
                            self,
                            'WARNING',
                            "Preview unavailable: {error}",
                            error=exc,
                        )

                    self._area.tag_redraw()
                    return {'RUNNING_MODAL'}

                # Keep the camera unchanged during a single stroke.
                return {'RUNNING_MODAL'}

            if (
                event.type in {'RET', 'NUMPAD_ENTER'}
                and event.value == 'PRESS'
            ):
                if not self._selected_count:
                    report_user(
                        self,
                        'WARNING',
                        "Draw a stroke that touches "
                        "at least one valid section loop.",
                    )
                    return {'RUNNING_MODAL'}

                try:
                    count, cap_seams = self._commit_cut(context)


                except Exception as exc:
                    # Rejected cuts retain the preview and the untouched source.
                    report_user(
                        self,
                        'ERROR',
                        "Freehand cut was not completed: {error}",
                        error=exc,
                    )
                    return {'RUNNING_MODAL'}

                self._cleanup()

                # Report the actual boundary state of the published parts.
                message = (
                    "Freehand cut created {count} closed parts. "
                    "The unchanged original was hidden."
                    if cap_seams
                    else
                    "Freehand cut created {count} parts with open cut boundaries. "
                    "The unchanged original was hidden."
                )

                report_user(
                    self,
                    'INFO',
                    message,
                    count=count,
                )

                return {'FINISHED'}

            navigation = {
                'MIDDLEMOUSE',
                'WHEELUPMOUSE',
                'WHEELDOWNMOUSE',
                'TRACKPADPAN',
                'TRACKPADZOOM',
                'MOUSEROTATE',
                'MOUSESMARTZOOM',
                'NDOF_MOTION',
                'NUMPAD_0',
                'NUMPAD_1',
                'NUMPAD_2',
                'NUMPAD_3',
                'NUMPAD_4',
                'NUMPAD_5',
                'NUMPAD_6',
                'NUMPAD_7',
                'NUMPAD_8',
                'NUMPAD_9',
                'NUMPAD_PERIOD',
                'NUMPAD_PLUS',
                'NUMPAD_MINUS',
            }

            if event.type in navigation:
                return {'PASS_THROUGH'}

            if event.type == 'MOUSEMOVE':
                return {'PASS_THROUGH'}

            # Block editing shortcuts while the source-dependent preview runs.
            return {'RUNNING_MODAL'}

        except Exception as exc:
            report_user(
                self,
                'ERROR',
                "Freehand Cut failed: {error}",
                error=exc,
            )
            self._cleanup()
            return {'CANCELLED'}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_CLASSES = (SNAP_OT_freehand_cut,)


def register():
    """Register the combined preview and local cutting operator."""
    for cls in _CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Close active previews before unregistering the operator class."""
    for operator in tuple(_ACTIVE_OPERATORS):
        operator._cleanup()

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
```

---

### ops_split.py

```py
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# ops_split.py

import bpy
import bmesh
from bpy.types import Operator
from bpy.app.handlers import persistent
from mathutils import Vector, Matrix
from datetime import datetime

from .utils import (
    ensure_collection,
    report_user,
    is_lang_de,
    unit_mm,
)

from .utils import _trf

# Import translation helper
# 'tr' resolves UI strings from a central language dictionary.
# It accepts a key and a default English fallback text.


# ---------------------------
# Preview naming
# ---------------------------

PREVIEW_COLL_NAME = "_SnapSplit_Preview"
PREVIEW_PLANE_PREFIX = "_SnapSplit_PreviewPlane_"
PREVIEW_MAT_NAME = "_SnapSplit_Preview_MAT"

# ---------------------------
# bpy.ops fallback policy (documented for Extensions review)
# ---------------------------
# Blender's own "Select Edge Loop" walker (bpy.ops.mesh.loop_multi_select) is
# implemented in C and has no 1:1 public Python/BMesh equivalent.
# SnapSplit therefore first tries a conservative pure-BMesh loop walker
# (_walk_edge_loop_closed) that only accepts results which form a CLOSED cycle.
# Only if the walker cannot prove a closed cycle (e.g. n-gon stars, triangle
# fans, non-manifold pinch points) we fall back to the operator for exactly
# this single special case. Set to False to disable the fallback entirely.
_ALLOW_OPS_LOOP_FALLBACK = True

# ---------------------------
# Helpers: AABB / axes / eps / context / normals
# ---------------------------

def axis_index_for(axis):
    """Return axis index 0/1/2 for axis string X/Y/Z."""
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def world_aabb(obj):
    """Return world-space axis-aligned bounding-box (min,max) for object."""
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v

def aabb_center(min_v, max_v):
    """Return center point of an AABB defined by min_v and max_v."""
    return 0.5 * (min_v + max_v)

def world_pos_from_norm(obj, axis, t_norm):
    """Map t_norm in [-1, 1] to a world position along the object's AABB on the given axis."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    lo = min_v[ax]; hi = max_v[ax]
    mid = 0.5 * (lo + hi); half = 0.5 * (hi - lo)
    return mid + t_norm * half, (lo, hi, mid, half)

def size_on_tangential_axes(obj, axis):
    """Return lengths on the two tangential axes relative to the split axis."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    t1 = (ax + 1) % 3; t2 = (ax + 2) % 3
    return (abs(max_v[t1] - min_v[t1]), abs(max_v[t2] - min_v[t2])), (t1, t2), (min_v, max_v)

def _diag_eps(obj, k=1e-6, min_eps=1e-6):
    """Return an epsilon scaled by the object's diagonal length (clamped by min_eps)."""
    min_v, max_v = world_aabb(obj)
    diag = (max_v - min_v).length
    return max(min_eps, diag * k)

def _ensure_object_mode():
    """Ensure Blender is in OBJECT mode (safe switch if needed)."""
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    try:
        ob = bpy.context.object
        if ob and ob.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

def _deselect_all_objects():
    """Deselect all objects of the current view layer via RNA (replaces bpy.ops.object.select_all)."""
    try:
        view_layer = bpy.context.view_layer
        for o in list(view_layer.objects):
            try:
                # select_set() is a cheap RNA call; hidden objects may refuse it, which is fine
                o.select_set(False)
            except Exception:
                pass
    except Exception:
        pass

def _activate_single_object(obj):
    """Activate and exclusively select a single object."""
    _ensure_object_mode()
    _deselect_all_objects()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def _enter_edit_mode_edges(obj):
    """Enter EDIT mode on obj and switch selection mode to EDGE."""
    _activate_single_object(obj)
    # Set the EDGE select mode through tool settings BEFORE entering Edit Mode.
    # The edit-mesh is created with this mode, so the operator
    # bpy.ops.mesh.select_mode(type='EDGE') is no longer needed.
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
    except Exception:
        pass
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    bpy.ops.object.mode_set(mode='EDIT')

def _leave_edit_mode():
    """Leave EDIT mode if currently active."""
    try:
        if bpy.context.object and bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

def warn_if_unapplied_transforms(obj, operator=None):
    """Report a non-blocking info message if object has unapplied transforms that may affect splitting."""
    if not obj or obj.type != 'MESH':
        return
    try:
        loc = tuple(getattr(obj, "location", (0.0, 0.0, 0.0)))
        has_loc = any(abs(v) > 1e-7 for v in loc)

        has_rot = False
        rot_mode = getattr(obj, "rotation_mode", "QUATERNION")
        if rot_mode == 'QUATERNION':
            q = getattr(obj, "rotation_quaternion", None)
            if q is not None:
                has_rot = (abs(q.w - 1.0) > 1e-7) or (abs(q.x) > 1e-7) or (abs(q.y) > 1e-7) or (abs(q.z) > 1e-7)
        else:
            e = getattr(obj, "rotation_euler", None)
            if e is not None:
                has_rot = any(abs(a) > 1e-7 for a in (e.x, e.y, e.z))

        sx, sy, sz = getattr(obj, "scale", (1.0, 1.0, 1.0))
        non_uniform = (abs(sx - sy) > 1e-7) or (abs(sy - sz) > 1e-7) or (abs(sx - sz) > 1e-7)
        det = obj.matrix_world.to_3x3().determinant()
        negative_scale = det < 0.0

        if has_loc or has_rot or non_uniform or negative_scale:
            # Build bilingual message via translation keys
            details = []
            if has_loc: details.append('Location')
            if has_rot: details.append('Rotation')
            if non_uniform: details.append('Non-uniform Scale')
            if negative_scale: details.append('Negative Scale')
            details_str = ", ".join(details)

            msg = 'Object has unapplied transforms'
            hint = 'Consider Apply All Transforms (Ctrl+A) for exact and predictable split results.'
            msg_all = f"{msg}: {details_str}. {hint}"

            if operator is not None:
                report_user(operator, 'INFO', msg_all)
            else:
                print(f"[SnapSplit] {msg_all}")
    except Exception:
        pass

# ---------------------------
# Depsgraph handler
# ---------------------------

_last_preview_active_obj = None

# Separate, independent state for the connector live-preview branch below.
# Kept as a simple tuple signature of selected mesh object names so we can
# cheaply detect "selection changed" without depending on the split-preview
# state above. None means "not initialized yet" (forces an initial check).
_last_connector_preview_selection_key = None

@persistent  # survive file loads; lifetime is managed by sync_depsgraph_handler()
def _snapsplit_depsgraph_update(scene, depsgraph):
    """Depsgraph post-update handler to refresh preview planes/objects on relevant data changes.

    This handler drives two fully independent preview systems:
      1) The split-plane preview (unchanged, reacts to active-object changes
         and depsgraph updates on that object/its mesh data).
      2) The connector placement live preview (new), which reacts only to
         changes in the current selection set and is entirely gated by its
         own 'connector_live_preview' toggle. Neither branch's early-return
         affects the other, so turning off "Show split preview" no longer
         disables the connector live preview and vice versa.
    """
    global _last_preview_active_obj, _last_connector_preview_selection_key

    props = getattr(scene, "snapsplit", None)
    ctx = bpy.context

    # --- Branch 1: split-plane preview (unchanged behavior) ---
    if 'update_split_preview_plane' not in globals():
        pass
    elif not props or not getattr(props, "show_split_preview", False):
        _last_preview_active_obj = None
    else:
        obj = ctx.active_object

        if obj is not _last_preview_active_obj:
            try:
                update_split_preview_plane(ctx)
            except Exception:
                pass
            _last_preview_active_obj = obj
        elif obj:
            try:
                for up in depsgraph.updates:
                    id_orig = getattr(up.id, "original", None)
                    if id_orig is obj or id_orig is obj.data:
                        update_split_preview_plane(ctx)
                        break
            except Exception:
                pass

    # --- Branch 2: connector placement live preview (new, independent) ---
    if not props or not getattr(props, "connector_live_preview", False):
        # Reset the tracked selection so a fresh selection is always detected
        # once the toggle is switched back on.
        _last_connector_preview_selection_key = None
        return

    try:
        sel_key = tuple(sorted(o.name for o in ctx.selected_objects if o.type == 'MESH'))
    except Exception:
        sel_key = None

    if sel_key != _last_connector_preview_selection_key:
        _last_connector_preview_selection_key = sel_key
        try:
            from . import ops_connectors
            ops_connectors.update_connector_placement_preview(ctx)
        except Exception:
            pass

_DEPSGRAPH_HANDLER_NAME = "_snapsplit_depsgraph_update"
_LOAD_HANDLER_NAME = "_snapsplit_load_post"


def _find_handlers_named(handler_list, name):
    """Return all handlers in 'handler_list' with the given function name defined in THIS module.

    Matching by name + module (not by object identity) also catches stale function
    objects left over from importlib.reload() during development.
    """
    return [h for h in handler_list
            if getattr(h, "__name__", "") == name
            and getattr(h, "__module__", "") == __name__]


def _remove_handlers_named(handler_list, name):
    """Remove every SnapSplit handler called 'name' from 'handler_list'. Returns the count removed."""
    found = _find_handlers_named(handler_list, name)
    for h in found:
        try:
            handler_list.remove(h)
        except ValueError:
            pass
    return len(found)


def _any_live_preview_enabled():
    """Return True if any scene has the split preview or the connector live preview enabled."""
    try:
        for sc in bpy.data.scenes:
            p = getattr(sc, "snapsplit", None)
            if p and (getattr(p, "show_split_preview", False)
                      or getattr(p, "connector_live_preview", False)):
                return True
    except Exception:
        # bpy.data can be restricted while an add-on registers; treat as "nothing enabled".
        # The load_post handler (or the next toggle) re-syncs later.
        pass
    return False


def sync_depsgraph_handler():
    """Attach the depsgraph handler while a live preview is enabled, detach it otherwise.

    Called from the update callbacks of the two preview toggles, from the load_post
    handler and from register(). Cheap: it only scans the scenes for two booleans.
    """
    global _last_preview_active_obj, _last_connector_preview_selection_key

    handlers = bpy.app.handlers.depsgraph_update_post
    wanted = _any_live_preview_enabled()
    present = bool(_find_handlers_named(handlers, _DEPSGRAPH_HANDLER_NAME))

    if wanted and not present:
        handlers.append(_snapsplit_depsgraph_update)
    elif not wanted and present:
        _remove_handlers_named(handlers, _DEPSGRAPH_HANDLER_NAME)
        # Reset the change-tracking state so the next enable starts with a fresh initial check
        _last_preview_active_obj = None
        _last_connector_preview_selection_key = None


@persistent  # must outlive file loads, otherwise it would be removed right when it is needed
def _snapsplit_load_post(_filepath=None):
    """After a file load, re-sync the depsgraph handler with the preview toggles saved in the file.

    Property update callbacks do not fire when a .blend is loaded, so a file saved with
    a preview enabled would otherwise come back without a working handler.
    """
    try:
        sync_depsgraph_handler()
    except Exception as e:
        print(f"[SnapSplit] Could not sync depsgraph handler after load: {e}")

# ---------------------------
# Preview material/planes
# ---------------------------

def update_split_preview_plane(context):
    """Create/refresh or remove split preview planes when UI properties change."""
    try:
        scene = context.scene
        props = getattr(scene, "snapsplit", None)
        obj = context.active_object
        if not props:
            return

        show = bool(getattr(props, "show_split_preview", False))
        axis = getattr(props, "split_axis", "Z")
        parts_count = max(2, int(getattr(props, "parts_count", 2)))
        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

        if show and obj and obj.type == 'MESH':
            # Build/refresh preview planes for the current active object
            position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=True)
        else:
            # Turn off and clean up any preview planes
            _disable_split_preview_and_cleanup(context)
    except Exception:
        # Be robust against any context changes
        pass

def build_orange_preview_material():
    """Create or reuse the translucent orange preview material."""
    name = PREVIEW_MAT_NAME
    mat = bpy.data.materials.get(name)
    if mat: return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (200, 0)
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (0, 0)
    transp = nt.nodes.new("ShaderNodeBsdfTransparent"); transp.location = (-200, -100)
    emis = nt.nodes.new("ShaderNodeEmission"); emis.location = (-200, 100)
    emis.inputs["Color"].default_value = (1.0, 0.5, 0.0, 1.0)
    emis.inputs["Strength"].default_value = 3.0
    fac = nt.nodes.new("ShaderNodeValue"); fac.location = (-400, 0)
    fac.outputs[0].default_value = 0.3
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(transp.outputs[0], mix.inputs[1])
    nt.links.new(emis.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = False
    return mat

def ensure_preview_collection():
    """Ensure the preview collection exists and return it."""
    coll = bpy.data.collections.get(PREVIEW_COLL_NAME)
    if coll is None:
        coll = bpy.data.collections.new(PREVIEW_COLL_NAME)
        bpy.context.scene.collection.children.link(coll)
    return coll

def create_or_get_preview_plane(context, obj, axis, name):
    """Create or fetch a named preview plane and ensure it has the preview material."""
    coll = ensure_preview_collection()
    plane = bpy.data.objects.get(name)
    if plane is None or plane.type != 'MESH':
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        bm.to_mesh(me); bm.free()
        plane = bpy.data.objects.new(name, me)
        coll.objects.link(plane)

    mat = build_orange_preview_material()
    if not plane.data.materials:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat

    plane.hide_set(False)
    plane.hide_viewport = False
    plane.show_in_front = False
    plane.display_type = 'TEXTURED'
    plane.show_wire = True
    plane.show_all_edges = True
    plane.hide_select = True
    try: plane.color = (1.0, 0.1, 0.1, 1.0)
    except Exception: pass
    return plane

def preview_plane_name_for(obj_name: str, idx: int) -> str:
    """Return a unique preview plane name for an object and index."""
    return f"{PREVIEW_PLANE_PREFIX}{obj_name}_{idx}"

def preview_plane_names_for_object(obj_name: str, parts_count: int):
    """Return all expected preview plane names for an object given parts_count."""
    n = max(0, int(parts_count) - 1)
    return [preview_plane_name_for(obj_name, i+1) for i in range(n)]

def build_preview_matrix(obj, axis, pos):
    """Build a world matrix for a preview plane sized to object tangential extents at position pos."""
    (size_t1, size_t2), (t1_idx, t2_idx), (min_v, max_v) = size_on_tangential_axes(obj, axis)
    size_t1 = max(size_t1, 1e-9); size_t2 = max(size_t2, 1e-9)
    ax = axis_index_for(axis); c = aabb_center(min_v, max_v)
    world_axes = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))
    z_dir = world_axes[ax].copy().normalized()
    x_dir = world_axes[t1_idx].copy().normalized()
    if abs(z_dir.dot(x_dir)) > 0.999:
        x_dir = world_axes[(ax + 2) % 3].copy().normalized()
    y_dir = z_dir.cross(x_dir)
    if y_dir.length_squared == 0.0:
        x_dir = world_axes[(ax + 2) % 3].copy().normalized()
        y_dir = z_dir.cross(x_dir)
    y_dir.normalize(); x_dir = y_dir.cross(z_dir); x_dir.normalize()
    R = Matrix(((x_dir.x, y_dir.x, z_dir.x, 0.0),
                (x_dir.y, y_dir.y, z_dir.y, 0.0),
                (x_dir.z, y_dir.z, z_dir.z, 0.0),
                (0.0,     0.0,     0.0,     1.0)))
    S = Matrix.Diagonal(Vector((size_t1, size_t2, 1.0, 1.0)))
    tloc = Vector((c.x, c.y, c.z)); tloc[ax] = pos
    T = Matrix.Translation(tloc)
    return T @ R @ S

def position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=False):
    """Create/update preview planes for an object based on axis, parts_count and offset."""
    if not obj or obj.type != 'MESH':
        return
    obj_name = obj.name
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    length = max_v[ax] - min_v[ax]

    targets = []
    if length > 0.0 and parts_count >= 2:
        for i in range(1, parts_count):
            t = i / parts_count
            pos = min_v[ax] + t * length + offset_scene
            pos = max(min_v[ax], min(max_v[ax], pos))
            targets.append(pos)

    want_names = preview_plane_names_for_object(obj_name, parts_count)

    if force_rebuild:
        for o in [o for o in bpy.data.objects if o.name.startswith(f"{PREVIEW_PLANE_PREFIX}{obj_name}_")]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    for name, pos in zip(want_names, targets):
        plane = bpy.data.objects.get(name)
        if plane is None:
            plane = create_or_get_preview_plane(context, obj, axis, name)
        plane.matrix_world = build_preview_matrix(obj, axis, pos)
        plane.hide_set(False)
        plane.hide_viewport = False
        plane.display_type = 'TEXTURED'
        plane.show_wire = True
        plane.show_all_edges = True
        try: plane.color = (1.0, 0.1, 0.1, 1.0)
        except Exception: pass

    existing_scoped = [o for o in bpy.data.objects if o.name.startswith(f"{PREVIEW_PLANE_PREFIX}{obj_name}_")]
    for o in existing_scoped:
        if o.name not in want_names:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    stray = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX) and f"{obj_name}_" not in o.name]
    for o in stray:
        for coll in list(o.users_collection):
            try: coll.objects.unlink(o)
            except Exception: pass
        try:
            bpy.data.objects.remove(o)
        except Exception: pass

def _disable_split_preview_and_cleanup(context):
    """Disable the split preview toggle and remove all preview planes and empty collections."""
    # Give the viewport's X-Ray state back (no-op if the cut preview never switched it on)
    try:
        from .utils import xray_release
        xray_release("split_preview")
    except Exception:
        pass
    try:
        props = getattr(context.scene, "snapsplit", None)

        if props and getattr(props, "show_split_preview", False):
            props.show_split_preview = False
    except Exception:
        pass
    try:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass
    except Exception:
        pass
    try:
        pc = bpy.data.collections.get(PREVIEW_COLL_NAME)
        if pc and len(pc.objects) == 0:
            for sc in bpy.data.scenes:
                try:
                    if pc in sc.collection.children:
                        sc.collection.children.unlink(pc)
                except Exception:
                    pass
            try: bpy.data.collections.remove(pc)
            except Exception: pass
    except Exception:
        pass

# ---------------------------
# Job collection management (Parts / Helpers)
# ---------------------------

def _ensure_root_collection(name, hide=False):
    """Ensure a top-level root collection exists (optionally hidden in viewport)."""
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    # Best-effort: set viewport hidden state on the LayerCollection
    try:
        for sc in bpy.data.scenes:
            lay = sc.view_layers[0] if sc.view_layers else None
            if not lay:
                continue
            def _mark(layer_coll, target, hide_flag):
                if layer_coll.collection == target:
                    layer_coll.hide_viewport = hide_flag
                    return True
                for ch in layer_coll.children:
                    if _mark(ch, target, hide_flag):
                        return True
                return False
            _mark(lay.layer_collection, coll, hide)
    except Exception:
        pass
    return coll

def _ensure_job_collections(source_name):
    """Create per-job Parts and Helpers collections under SnapSplit_Parts and SnapSplit_Helpers roots."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    parts_root   = _ensure_root_collection("SnapSplit_Parts",   hide=False)
    helpers_root = _ensure_root_collection("SnapSplit_Helpers", hide=True)

    parts_job   = bpy.data.collections.new(f"{source_name}_{ts}")
    helpers_job = bpy.data.collections.new(f"{source_name}_{ts}")

    parts_root.children.link(parts_job)
    helpers_root.children.link(helpers_job)

    # Ensure visibility flags: parts visible, helpers hidden
    try:
        for sc in bpy.data.scenes:
            lay = sc.view_layers[0] if sc.view_layers else None
            if not lay:
                continue
            def _mark(layer_coll, target, hide_flag):
                if layer_coll.collection == target:
                    layer_coll.hide_viewport = hide_flag
                    return True
                for ch in layer_coll.children:
                    if _mark(ch, target, hide_flag):
                        return True
                return False
            _mark(lay.layer_collection, parts_job,   False)
            _mark(lay.layer_collection, helpers_job, True)
    except Exception:
        pass

    return parts_job, helpers_job

def _move_objs_to_collection(objs, target_coll, hide=True, unlink_first=True):
    """Move objects to target collection and set object viewport hidden if requested."""
    for o in list(objs):
        if not o or o.__class__.__name__ != "Object":
            continue
        if unlink_first:
            for c in list(o.users_collection):
                try: c.objects.unlink(o)
                except Exception: pass
        try:
            if target_coll not in o.users_collection:
                target_coll.objects.link(o)
        except Exception:
            pass
        try:
            o.hide_set(bool(hide))
        except Exception:
            pass

# ---------------------------
# Hollow Preparation (modifier or separate inner/outer object)
# ---------------------------

def _is_hollow_like_modifier(m):
    """Return True for modifiers considered 'hollow-like' (certain node groups or Solidify)."""
    n = (m.name or "").lower()
    # Treat nodes-based Hollow/Print3D by name
    if (m.type == 'NODES') and ("hollow" in n or "print3d" in n or "print 3d" in n):
        return True
    # Explicitly treat Solidify as hollow-like
    if m.type == 'SOLIDIFY':
        return True
    return False

def _try_apply_hollow_modifier(obj):
    """Attempt to apply all hollow-like modifiers on obj; return True if any was applied."""
    # Note: applying in reverse order to respect modifier stack
    mods = [m for m in obj.modifiers if _is_hollow_like_modifier(m)]
    ok_any = False
    for m in reversed(mods):
        ok_any |= _apply_modifier(obj, m)
    return ok_any

def _apply_modifier(obj, mod):
    """Apply a single modifier and report success."""
    _activate_single_object(obj)
    try:
        # Kept on purpose as bpy.ops: Hollow/Solidify/Geometry-Nodes results are not yet
        # verified with the data-based apply (see apply_modifier_data in utils.py).

        bpy.ops.object.modifier_apply(modifier=mod.name)
        return True
    except Exception as e:
        print(f"[SnapSplit] Apply modifier '{mod.name}' failed: {e}")
        return False

def _find_paired_inner_object_for(obj):
    """Heuristic to find inner/outer paired mesh: similar name, same location, similar AABB center, slightly smaller/larger."""
    base = obj.name.lower()
    min_v, max_v = world_aabb(obj)
    diag = (max_v - min_v).length
    cand = []
    for o in bpy.context.scene.objects:
        if o is obj or o.type != 'MESH':
            continue
        n = o.name.lower()
        if base in n or n.replace(" ", "").startswith(base.replace(" ", "")):
            min_i, max_i = world_aabb(o)
            diag_i = (max_i - min_i).length
            # inner: 0.2*diag < diag_i < 0.98*diag, outer possibly > 1.02*diag
            if (0.2 * diag < diag_i < 0.98 * diag) or (diag_i > 1.02 * diag):
                if (o.location - obj.location).length < max(1e-6, diag * 1e-4):
                    cand.append((abs(diag - diag_i), o))
    cand.sort(key=lambda t: t[0])
    return cand[0][1] if cand else None

def _join_objects_via_operator(main_obj, other_obj):
    """DOCUMENTED FALLBACK: join via bpy.ops.object.join (only used if the BMesh join fails)."""
    _activate_single_object(main_obj)
    other_obj.select_set(True)
    try:
        bpy.ops.object.join()
    except Exception as e:
        print(f"[SnapSplit] Join failed: {e}")
    return main_obj


def _join_objects(main_obj, other_obj):
    """Join other_obj into main_obj with BMesh (replaces object.join) and return main_obj.

    other_obj is transformed into the local space of main_obj, appended to its mesh and
    then removed from the file (like the operator does). Materials are merged by slot.
    On any error nothing is written and the operator fallback is used.
    """
    # Keep the side effect of the old code: main_obj ends up active and selected
    _activate_single_object(main_obj)

    if (other_obj is None or other_obj is main_obj
            or main_obj.type != 'MESH' or other_obj.type != 'MESH'):
        return main_obj

    tmp_mesh = None
    try:
        # BMesh I/O only works on Object Mode mesh data
        if main_obj.mode != 'OBJECT' or other_obj.mode != 'OBJECT':
            raise RuntimeError("objects must be in Object Mode")

        # Shared mesh data would change other users too: give main_obj its own copy
        if main_obj.data.users > 1:
            main_obj.data = main_obj.data.copy()

        # Map the material slots of other_obj onto main_obj (append missing ones)
        remap = {}
        main_mats = main_obj.data.materials
        for i, mat in enumerate(other_obj.data.materials):
            if mat is None:
                continue
            existing = [m for m in main_mats]
            if mat in existing:
                remap[i] = existing.index(mat)
            else:
                main_mats.append(mat)
                remap[i] = len(main_mats) - 1

        # Copy other_obj's mesh into main_obj's local space
        rel = main_obj.matrix_world.inverted() @ other_obj.matrix_world
        bm_other = bmesh.new()
        try:
            bm_other.from_mesh(other_obj.data)
            bmesh.ops.transform(bm_other, matrix=rel, verts=bm_other.verts)
            if rel.determinant() < 0.0:
                # Mirrored transform flips the winding: restore outward-facing faces
                bmesh.ops.reverse_faces(bm_other, faces=bm_other.faces[:])
            for f in bm_other.faces:
                f.material_index = remap.get(f.material_index, f.material_index)
            tmp_mesh = bpy.data.meshes.new("_SnapSplit_join_tmp")
            bm_other.to_mesh(tmp_mesh)
        finally:
            bm_other.free()

        # Append to main_obj's mesh (BMesh.from_mesh adds to existing geometry)
        bm = bmesh.new()
        try:
            bm.from_mesh(main_obj.data)
            bm.from_mesh(tmp_mesh)
            bm.to_mesh(main_obj.data)
        finally:
            bm.free()
        main_obj.data.update()

        # Remove the joined object and its orphaned mesh, like the operator does
        other_mesh = other_obj.data
        bpy.data.objects.remove(other_obj, do_unlink=True)
        if other_mesh is not None and other_mesh.users == 0:
            bpy.data.meshes.remove(other_mesh)
        return main_obj

    except Exception as e:
        print(f"[SnapSplit] BMesh join failed ({e}); falling back to bpy.ops.object.join")
        return _join_objects_via_operator(main_obj, other_obj)
    finally:
        if tmp_mesh is not None:
            try:
                bpy.data.meshes.remove(tmp_mesh)
            except Exception:
                pass


def _recalc_normals_outside(obj):
    """Recalculate face normals to point outward using BMesh only.

    Replaces the former sequence
        bpy.ops.mesh.select_all(action='SELECT') + bpy.ops.mesh.normals_make_consistent(inside=False)
    No Edit Mode round trip is needed. Works in OBJECT mode (mesh datablock is
    read into a temporary BMesh and written back) and, if the object happens to be
    in EDIT mode, directly on the edit BMesh.
    """
    if not obj or obj.type != 'MESH' or obj.data is None:
        return
    try:
        if obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bmesh.update_edit_mesh(obj.data)
        else:
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
                bm.to_mesh(obj.data)
            finally:
                bm.free()
            obj.data.update()
    except Exception as ex:
        print(f"[SnapSplit DEBUG] _recalc_normals_outside failed on '{getattr(obj, 'name', '?')}': {ex}")

def robust_prepare_hollow(obj, operator=None):
    """Normalize 'hollow' preparation: apply hollow-like modifiers or join detected inner/outer shell; return (obj, used_hollow)."""
    if not obj or obj.type != 'MESH':
        return obj, False

    used_hollow = False

    applied = _try_apply_hollow_modifier(obj)
    if applied:
        used_hollow = True

    partner = _find_paired_inner_object_for(obj) if not applied else None
    if partner is not None:
        used_hollow = True
        obj = _join_objects(obj, partner)
        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass
        _enter_edit_mode_edges(obj)
        bm = bmesh.from_edit_mesh(obj.data)
        try:
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=_diag_eps(obj, k=2e-6, min_eps=1e-6))
        except Exception:
            pass
        bmesh.update_edit_mesh(obj.data)
        _leave_edit_mode()

    _recalc_normals_outside(obj)
    return obj, used_hollow

# ---------------------------
# Cuts with global offset
# ---------------------------

def create_cut_data_with_offset(obj, axis, parts_count, global_offset_scene=0.0):
    """Create a list of (plane_point_world, plane_normal_world) cuts with an additional global offset."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    length = max_v[ax] - min_v[ax]
    if length <= 0.0 or parts_count < 2:
        return []
    cuts = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos = min_v[ax] + t * length + global_offset_scene
        pos = max(min_v[ax], min(max_v[ax], pos))
        if axis == "X":
            no_world = Vector((1, 0, 0)); co_world = Vector((pos, 0, 0))
        elif axis == "Y":
            no_world = Vector((0, 1, 0)); co_world = Vector((0, pos, 0))
        else:
            no_world = Vector((0, 0, 1)); co_world = Vector((0, 0, pos))
        cuts.append((co_world, no_world))
    return cuts

# ---------------------------
# Split (BMesh)
# ---------------------------

def _order_cycle_verts(loop_edges):
    """Return the vertices of a closed edge cycle in walking order, or None if it is not a simple cycle."""
    adj = {}
    for e in loop_edges:
        a, b = e.verts
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    # A simple closed cycle has exactly two neighbours per vertex
    if not adj or any(len(n) != 2 for n in adj.values()):
        return None
    start = next(iter(adj))
    ordered = [start]
    prev, cur = None, start
    while True:
        n0, n1 = adj[cur]
        # NOTE: use == (not 'is'): BMesh Python wrappers are not guaranteed to be identical objects
        nxt = n0 if (prev is None or n0 != prev) else n1
        if nxt == start:
            break
        ordered.append(nxt)
        prev, cur = cur, nxt
        if len(ordered) > len(adj):
            return None
    return ordered if len(ordered) == len(adj) else None


def _poly_area_2d(pts):
    """Return the absolute area of a 2D polygon (shoelace formula)."""
    s = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) * 0.5


def _point_in_poly_2d(pt, poly):
    """Return True if a 2D point lies inside a 2D polygon (ray casting)."""
    x, y = pt
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            x_cross = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < x_cross:
                inside = not inside
        j = i
    return inside


def _group_loops_by_nesting(loops, ax):
    """Group closed loops of ONE cut plane into 'outer loop + its direct holes'.

    Loops are projected to 2D by dropping the split axis 'ax'. A loop is a hole
    when it is enclosed by an odd number of other loops, an outer boundary when
    enclosed by an even number (islands inside cavities are handled correctly).
    Returns a list of dicts {'edges', 'n_holes', 'expected_area'} or None when a
    loop cannot be ordered (caller then falls back to the legacy behaviour).
    """
    t1, t2 = (ax + 1) % 3, (ax + 2) % 3
    infos = []
    for lp in loops:
        ordered = _order_cycle_verts(lp)
        if ordered is None or len(ordered) < 3:
            return None
        pts = [(v.co[t1], v.co[t2]) for v in ordered]
        infos.append({'edges': lp, 'pts': pts, 'area': _poly_area_2d(pts)})

    n = len(infos)
    for j in range(n):
        containers = [i for i in range(n)
                      if i != j
                      and infos[i]['area'] > infos[j]['area']
                      and _point_in_poly_2d(infos[j]['pts'][0], infos[i]['pts'])]
        infos[j]['depth'] = len(containers)
        # Direct parent = smallest loop that still contains this one
        infos[j]['parent'] = min(containers, key=lambda i: infos[i]['area']) if containers else None

    groups = []
    for j, info in enumerate(infos):
        if info['depth'] % 2 != 0:
            continue  # holes are attached to their outer loop below
        holes = [k for k, o in enumerate(infos) if o['depth'] % 2 == 1 and o['parent'] == j]
        edges = list(info['edges'])
        for k in holes:
            edges += infos[k]['edges']
        expected = info['area'] - sum(infos[k]['area'] for k in holes)
        groups.append({'edges': edges, 'n_holes': len(holes), 'expected_area': expected})
        print(f"[SnapSplit DEBUG]   nesting: outer loop #{j} (area={info['area']:.5f}) "
              f"with {len(holes)} hole(s), expected cap area={expected:.5f}")
    return groups


def _fill_nested_group_bmesh(bm, edges, n_plane, n_holes, expected_area):
    """Fill 'outer loop + holes' and verify the result, leaving holes open.

    Tries several triangle_fill variants (the first mimics Mesh > Fill, which works
    in the manual 'Cap seams now' path). After each attempt the created face area is
    compared with the expected ring area; a cap that also covers a hole is deleted
    again. The last resort for exactly one hole is bridge_loops, which can never fill
    the hole. Returns True on success, False if the group was left open.
    """
    variants = (
        dict(use_beauty=True, use_dissolve=False),
        dict(use_beauty=True, use_dissolve=False, normal=n_plane),
        dict(use_beauty=True, use_dissolve=True, normal=n_plane),
    )
    for vi, kwargs in enumerate(variants):
        try:
            res = bmesh.ops.triangle_fill(bm, edges=edges, **kwargs)
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} raised: {ex}")
            continue
        faces = [g for g in res.get('geom', []) if isinstance(g, bmesh.types.BMFace)]
        if not faces:
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi}: no faces created")
            continue
        area = sum(f.calc_area() for f in faces)
        if expected_area is None or abs(area - expected_area) <= max(0.02 * abs(expected_area), 1e-12):
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} OK: {len(faces)} face(s), area={area:.5f}")
            return True
        print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} REJECTED: area={area:.5f} "
              f"but expected {expected_area:.5f} (a hole was probably filled) -> removing faces")
        try:
            # context='FACES' also removes the diagonal edges created by the fill;
            # the loop edges survive because they still belong to the wall faces.
            bmesh.ops.delete(bm, geom=faces, context='FACES')
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     could not remove rejected faces: {ex}")
            return False

    if n_holes == 1:
        try:
            res = bmesh.ops.bridge_loops(bm, edges=edges, use_pairs=False, use_cyclic=False,
                                         use_merge=False, merge_factor=0.5, twist_offset=0)
            if res.get('faces'):
                print(f"[SnapSplit DEBUG]     bridge_loops fallback OK: {len(res['faces'])} face(s)")
                return True
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     bridge_loops fallback raised: {ex}")

    print("[SnapSplit][INFO]     group left OPEN (no fill variant produced a correct ring cap)")
    return False

def _fill_edges_bmesh(bm, edges, prefer_ngon=False, normal=None):
    """Fill the given boundary edges with BMesh only (replaces mesh.fill / fill_grid / edge_face_add).

    prefer_ngon=True : try contextual_create first (one N-gon, like edge_face_add),
                       then triangle_fill.
    prefer_ngon=False: triangle_fill only (what Mesh > Fill does; nested loops become
                       a ring with a hole).
    'normal' is an optional plane normal for a second triangle_fill attempt.
    Works on the given BMesh and ignores the selection. Returns True if a face was created.
    """
    edges = [e for e in edges if e.is_valid]
    if not edges:
        return False

    if prefer_ngon:
        try:
            res = bmesh.ops.contextual_create(bm, geom=edges)
            if [f for f in res.get('faces', []) if f.is_valid]:
                return True
        except Exception as ex:
            print(f"[SnapSplit DEBUG]   contextual_create raised: {ex}")

    variants = [dict(use_beauty=True, use_dissolve=False)]
    if normal is not None:
        variants.append(dict(use_beauty=True, use_dissolve=False, normal=normal))
    for kwargs in variants:
        try:
            res = bmesh.ops.triangle_fill(bm, edges=edges, **kwargs)
        except Exception as ex:
            print(f"[SnapSplit DEBUG]   triangle_fill raised: {ex}")
            continue
        if [g for g in res.get('geom', []) if isinstance(g, bmesh.types.BMFace)]:
            return True
    return False


def split_mesh_bmesh_into_two(source_obj, plane_co_obj, plane_no_obj, name_suffix="", do_fill=False):
    """Split a mesh into two halves by a plane in object space; optionally cap boundaries on each half."""
    _activate_single_object(source_obj)

    # Nudge the cutting plane by a tiny epsilon along its normal, BEFORE
    # bisecting, applied identically to both halves below. This resolves a
    # known bisect_plane degeneracy: if the requested plane coordinate
    # happens to pass EXACTLY through existing mesh vertices (e.g. a round
    # user-entered offset like 0 mm coinciding with Suzanne's own X=0
    # mirror-symmetry seam, or 400 mm coinciding by chance with an existing
    # cavity boundary edge loop), the resulting boundary can contain "pinch"
    # vertices where two otherwise-separate loops (outer silhouette and an
    # inner cavity/island contour) touch at exactly one point (degree 4
    # instead of 2). That breaks the strict-cycle assumption used by the
    # auto-cap loop detection, which either drops the affected loop entirely
    # or merges outer+inner into one loop that gets filled as a single solid
    # face -- sealing the whole cut plane shut. Nearby "non-round" offsets
    # (e.g. -10 mm, 350 mm) never hit this exact coincidence and therefore
    # worked correctly already. The nudge is far smaller than any meaningful
    # print tolerance, so it has no visible/dimensional effect.
    diag = max(source_obj.dimensions.length, 1e-6)
    eps_nudge = diag * 1e-5
    n_unit = plane_no_obj.normalized()
    plane_co_obj = plane_co_obj + n_unit * eps_nudge

    def make_half(keep_positive: bool):
        """Create one half (positive/negative side) of the split and return its Mesh datablock."""
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(
            bm, geom=geom,
            plane_co=plane_co_obj, plane_no=plane_no_obj,
            use_snap_center=False,
            clear_outer=not keep_positive,
            clear_inner=keep_positive
        )
        if do_fill:
            boundary_edges = [e for e in bm.edges if e.is_boundary]
            if boundary_edges:
                try:
                    bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
                except Exception:
                    pass
        bm.normal_update()
        me = bpy.data.meshes.new(f"{source_obj.name}_{'POS' if keep_positive else 'NEG'}{name_suffix}")
        bm.to_mesh(me); bm.free()
        return me

    me_pos = make_half(True)
    me_neg = make_half(False)

    target_coll = source_obj.users_collection[0] if source_obj.users_collection else bpy.context.scene.collection
    o_pos = bpy.data.objects.new(f"{source_obj.name}_A{name_suffix}", me_pos)
    o_neg = bpy.data.objects.new(f"{source_obj.name}_B{name_suffix}", me_neg)
    target_coll.objects.link(o_pos); target_coll.objects.link(o_neg)
    o_pos.matrix_world = source_obj.matrix_world.copy()
    o_neg.matrix_world = source_obj.matrix_world.copy()
    source_obj.hide_set(True)

    for o in (o_pos, o_neg):
        try:
            o.data.validate(False); o.data.update()
        except Exception:
            pass

    return o_pos, o_neg

def apply_bmesh_split_sequence(root_obj, axis, parts_count, cuts_override=None, operator=None):
    """Apply a sequence of planar splits on root_obj and return the resulting parts."""
    cuts = cuts_override if cuts_override is not None else create_cut_data_with_offset(root_obj, axis, parts_count, 0.0)
    if not cuts:
        return [root_obj]

    wm = bpy.context.window_manager
    wm.progress_begin(0, len(cuts))
    try:
        current_parts = [root_obj]
        for idx, (co_world, no_world) in enumerate(cuts, start=1):
            next_parts = []
            for part in current_parts:
                if part is None or part.type != 'MESH' or part.data is None:
                    continue

                try:
                    warn_if_unapplied_transforms(part, operator=operator)
                except Exception:
                    pass

                M = part.matrix_world; M_inv = M.inverted()
                co_obj = M_inv @ co_world
                no_obj = (M_inv.to_3x3().transposed() @ no_world)
                if no_obj.length_squared == 0.0:
                    continue
                if M.to_3x3().determinant() < 0.0:
                    no_obj.negate()
                no_obj.normalize()

                a, b = split_mesh_bmesh_into_two(part, co_obj, no_obj, name_suffix=f"_S{idx}", do_fill=False)
                if a and a.type == 'MESH': next_parts.append(a)
                if b and b.type == 'MESH': next_parts.append(b)

            current_parts = [p for p in next_parts if p and p.type == 'MESH' and p.data]

            wm.progress_update(idx)
            # Ask every 3D View to redraw (replaces bpy.ops.wm.redraw_timer).
            # NOTE: tag_redraw() only schedules the redraw. While execute() is blocking,
            # Blender may not repaint until the operator returns.
            try:
                for win in wm.windows:
                    for area in win.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
            except Exception:
                pass


        return [o for o in current_parts if o and o.type == 'MESH' and o.data and len(o.data.polygons) > 0]
    finally:
        wm.progress_end()

# ---------------------------
# Adjust split axis (modal preview)
# ---------------------------

class SNAP_OT_adjust_split_axis(Operator):
    """Interactively adjust split axis/offset with a live plane preview."""
    bl_idname = "snapsplit.adjust_split_axis"
    bl_label = "Adjust split axis"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        """Start modal adjustment, initialize preview planes and internal state."""
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        'Please select a mesh object.')
            return {'CANCELLED'}

        warn_if_unapplied_transforms(obj, operator=self)

        self.obj = obj
        self.props = context.scene.snapsplit
        self.axis = self.props.split_axis

        min_v, max_v = world_aabb(obj)
        ax = axis_index_for(self.axis)
        self.lo, self.hi = min_v[ax], max_v[ax]
        self.mid_world = 0.5 * (self.lo + self.hi)

        self.t_norm = 0.0
        try:
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            half = 0.5 * (self.hi - self.lo)
            if half > 1e-12:
                self.t_norm = max(-1.0, min(1.0, offset_scene / half))
        except Exception:
            pass

        self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)

        parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
        offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
        try:
            position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene, force_rebuild=True)
        except Exception:
            pass

        lead_name = preview_plane_name_for(self.obj.name, 1)
        try:
            self.preview_plane = create_or_get_preview_plane(context, self.obj, self.axis, lead_name)
            self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
        except Exception:
            self.preview_plane = None

        self._area = context.area; self._region = context.region

        # Keep the preview planes visible inside solid objects while adjusting
        try:
            from .utils import xray_acquire
            xray_acquire(context, "adjust_axis")
        except Exception:
            pass


        context.window_manager.modal_handler_add(self)
        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        """Stop modal mode, optionally remove preview planes and report status."""
        keep = False
        # Restore X-Ray (finish() is called on every exit path of the modal operator)
        try:
            from .utils import xray_release
            xray_release("adjust_axis")
        except Exception:
            pass

        try: keep = bool(getattr(context.scene.snapsplit, "show_split_preview", False))
        except Exception: pass
        if not keep:
            try:
                for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
                    for coll in list(o.users_collection):
                        try: coll.objects.unlink(o)
                        except Exception: pass
                    try: bpy.data.objects.remove(o)
                    except Exception: pass
            except Exception: pass
            _disable_split_preview_and_cleanup(context)

        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        msg_ok = 'Split axis adjusted.'
        msg_cancel = 'Adjust split axis cancelled.'
        report_user(self, 'INFO', msg_cancel if cancelled else msg_ok)

    def modal(self, context, event):
        """Handle mouse/keyboard events to adjust offset and update the preview."""
        if not self.obj or self.obj.name not in bpy.data.objects:
            self.finish(context, cancelled=True); return {'CANCELLED'}
        if event.type in {'ESC'}:
            self.finish(context, cancelled=True); return {'CANCELLED'}

        updated = False
        try:
            typed_mm = float(getattr(self.props, "split_offset_mm", 0.0))
            typed_scene = typed_mm * unit_mm()
            clamped_scene = max(self.lo - self.mid_world, min(self.hi - self.mid_world, typed_scene))
            half = 0.5 * (self.hi - self.lo) if (self.hi - self.lo) > 1e-12 else 1.0
            new_t = max(-1.0, min(1.0, clamped_scene / half))
            if abs(new_t - self.t_norm) > 1e-6:
                self.t_norm = new_t
                self.current_world_pos = self.mid_world + clamped_scene
                updated = True
        except Exception:
            pass

        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
            self.finish(context, cancelled=False); return {'FINISHED'}

        if event.type == 'MOUSEMOVE':
            dy = event.mouse_prev_y - event.mouse_y
            if dy != 0:
                self.t_norm = max(-1.0, min(1.0, self.t_norm - dy * 0.001))
                self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
                scene_units_offset = self.current_world_pos - self.mid_world
                self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
                updated = True

        step = 0.01
        if event.type in {'WHEELUPMOUSE', 'UP_ARROW'} and event.value == 'PRESS':
            self.t_norm = min(1.0, self.t_norm + step)
            self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
            scene_units_offset = self.current_world_pos - self.mid_world
            self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
            updated = True

        if event.type in {'WHEELDOWNMOUSE', 'DOWN_ARROW'} and event.value == 'PRESS':
            self.t_norm = max(-1.0, self.t_norm - step)
            self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
            scene_units_offset = self.current_world_pos - self.mid_world
            self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
            updated = True

        if updated:
            if getattr(self, "preview_plane", None):
                try: self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
                except ReferenceError: pass

            parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            try: position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception: pass

            try:
                if getattr(context.scene.snapsplit, "show_split_preview", False):
                    update_split_preview_plane(context)
            except Exception: pass

            if self._area: self._area.tag_redraw()
            if self._region:
                try: self._region.tag_redraw()
                except Exception: pass

        return {'RUNNING_MODAL'}

# ---------------------------
# Planar Split – prepare hollow, then split (+ optional auto-cap)
# ---------------------------

def _cap_single_object_simple_fill(obj) -> bool:
    """Fast legacy method: fill boundary loops using bmesh.ops.holes_fill."""
    try:
        me = obj.data
        bm = bmesh.new()
        bm.from_mesh(me)
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
            bm.normal_update()
            bm.to_mesh(me)
            me.update()
            bm.free()
            return True
        bm.free()
        return False
    except Exception:
        return False

def cap_single_object_hollow_style(obj) -> bool:
    """Cap boundary loops after Planar Split, correctly leaving cavities open.

    ARCHITECTURE CHANGE vs. previous session: instead of grouping raw
    boundary edges into position-based "cut-plane buckets" BEFORE trying to
    form loops (which fragments any boundary chain that drifts in position,
    e.g. an open mesh feature like Suzanne's un-capped nose hole, into many
    tiny non-cyclic buckets that get silently dropped), we now:

      1. Decompose ALL boundary edges into closed cycles and open chains
         GLOBALLY first (position-agnostic).
      2. Classify each closed cycle by its own planarity (max spread along
         the split axis). Planar cycles are real cut-plane loops and are
         kept. Non-planar cycles are closed rings that wander off the cut
         plane and back (e.g. a closed rim of a slanted pre-existing
         opening) and are explicitly excluded, with an INFO message instead
         of a silent drop.
      3. Open chains can never be filled (no closed loop exists), and are
         now explicitly reported via INFO instead of vanishing unnoticed
         inside the old per-bucket cycle decomposer. This is exactly the
         case of Suzanne's un-capped nose hole: its rim gets cut by the
         split into an open chain that is correctly left open, and the user
         now gets told why.
      4. Only the surviving planar closed loops are grouped into cut-plane
         buckets (by average position) for the existing single-loop /
         multi-loop (cavity ring) fill logic.

    Gap-stitching (bridging tiny EXACT-solver float gaps) now also runs
    ONCE globally instead of per tiny bucket, using bmesh.utils.edge_exists()
    (the correct API -- BMEdgeSeq has no .get() method).

    The whole body runs inside try/finally so _leave_edit_mode() is ALWAYS
    called, even on exception, to avoid corrupting the operator context for
    subsequent bpy.ops calls (previously observed crash in select_all).

    Step 1a/1b: the final select_all + normals_make_consistent operators were
    replaced by bmesh.ops.recalc_face_normals on the edit BMesh.
    """
    print(f"[SnapSplit DEBUG] ---- cap_single_object_hollow_style: {obj.name} ----")
    _enter_edit_mode_edges(obj)
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

    any_ok = False
    try:
        # Boundary vertex dedupe (unchanged from current version)
        boundary_verts = [v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
        print(f"[SnapSplit DEBUG] boundary verts before dedupe: {len(boundary_verts)}")
        if boundary_verts:
            try:
                dist = _diag_eps(obj, k=3e-6, min_eps=3e-7)
                bmesh.ops.remove_doubles(bm, verts=boundary_verts, dist=dist)
                bmesh.update_edit_mesh(obj.data)
                bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
                boundary_verts_after = [v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
                print(f"[SnapSplit DEBUG] boundary vertex dedupe: dist={dist:.6g}, "
                      f"boundary verts after={len(boundary_verts_after)}")
            except Exception as ex:
                print(f"[SnapSplit DEBUG] remove_doubles on boundary verts raised: {ex}")

        props = getattr(bpy.context.scene, "snapsplit", None)
        plane_axis = props.split_axis if props else "Z"

        ax = axis_index_for(plane_axis)
        axis_vecs = (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
        split_no = axis_vecs[ax].normalized()

        cand = [e for e in bm.edges if e.is_boundary]
        print(f"[SnapSplit DEBUG] total boundary edges (no direction filter): {len(cand)}")
        if not cand:
            print("[SnapSplit DEBUG] no candidate edges found -> abort")
            return False

        # ------------------------------------------------------------------
        # Global gap-stitching (runs ONCE over all boundary edges, not per
        # tiny position bucket -- avoids skewed min-edge-length thresholds).
        # ------------------------------------------------------------------
        def _stitch_dangling_endpoints_global(edges, bmesh_ref):
            """Bridge small gaps left by the EXACT boolean solver by
            connecting mutually-nearest dangling loop endpoints (odd-degree
            vertices) with new synthetic edges -- but only if the distance
            is small relative to the smallest existing boundary edge, so we
            never bridge a real, unrelated large gap (e.g. a pre-existing
            drain/access opening or an un-capped mesh feature like Suzanne's
            nose hole).
            """
            degree = {}
            for e in edges:
                for v in e.verts:
                    degree[v] = degree.get(v, 0) + 1
            dangling = [v for v, d in degree.items() if d % 2 == 1]
            print(f"[SnapSplit DEBUG]   dangling endpoints (global): {len(dangling)}")
            if len(dangling) < 2:
                return edges

            nearest = {}
            for v in dangling:
                best, bd = None, None
                for w in dangling:
                    if w is v:
                        continue
                    d = (v.co - w.co).length
                    if bd is None or d < bd:
                        bd, best = d, w
                nearest[v] = (best, bd)

            pairs, paired = [], set()
            for v in dangling:
                if v in paired:
                    continue
                w, d = nearest[v]
                if w is None or w in paired:
                    continue
                w_best, _ = nearest[w]
                if w_best is v:
                    pairs.append((v, w, d))
                    paired.add(v); paired.add(w)

            lens = [(e.verts[0].co - e.verts[1].co).length for e in edges]
            min_len = min(lens) if lens else 0.0
            max_stitch = max(min_len * 0.5, 1e-9)
            print(f"[SnapSplit DEBUG]   stitch safety threshold: {max_stitch:.6g} "
                  f"(global min boundary edge length: {min_len:.6g})")

            new_edges = list(edges)
            n_stitched = 0
            for v, w, d in pairs:
                ok = d <= max_stitch
                if ok:
                    existing = bmesh.utils.edge_exists(v, w)
                    new_e = existing if existing is not None else bmesh_ref.edges.new((v, w))
                    new_edges.append(new_e)
                    n_stitched += 1
            print(f"[SnapSplit DEBUG]   stitched {n_stitched} gap(s), "
                  f"rejected {len(pairs) - n_stitched} pair(s) as too far")
            bmesh_ref.edges.ensure_lookup_table()
            return new_edges

        cand = _stitch_dangling_endpoints_global(cand, bm)

        # ------------------------------------------------------------------
        # Global decomposition into closed cycles + open chains.
        # ------------------------------------------------------------------
        def _decompose_all_into_loops_and_chains_local(edges):
            """Split the full boundary edge set into closed cycles and open
            chains, globally (position-agnostic). Any connected chain that
            never closes back on itself (e.g. the rim of an un-capped mesh
            feature cut open by the split, such as Suzanne's nose hole) is
            returned separately as an "open chain" instead of being silently
            absorbed and lost, as the previous per-bucket decomposer did.
            """
            adj = {}
            remaining = set(edges)
            for e in edges:
                v0, v1 = e.verts
                adj.setdefault(v0, []).append((e, v1))
                adj.setdefault(v1, []).append((e, v0))

            def degree_in_remaining(v):
                return sum(1 for e, _ in adj.get(v, []) if e in remaining)

            # Step 1: peel off open chains starting at degree-1 vertices.
            open_chains = []
            while True:
                start_v = None
                for v in adj:
                    if degree_in_remaining(v) == 1:
                        start_v = v
                        break
                if start_v is None:
                    break
                chain_edges = []
                cur = start_v
                prev_edge = None
                while True:
                    nxt = None
                    for e, other in adj.get(cur, []):
                        if e in remaining and e is not prev_edge:
                            nxt = (e, other)
                            break
                    if nxt is None:
                        break
                    e, other = nxt
                    remaining.discard(e)
                    chain_edges.append(e)
                    prev_edge = e
                    cur = other
                    if degree_in_remaining(cur) != 2:
                        # Reached the opposite dangling end (or a branch
                        # point in degenerate non-manifold geometry) -> stop.
                        break
                if not chain_edges:
                    break
                open_chains.append(chain_edges)

            # Step 2: everything left should now form only closed cycles
            # (all remaining vertices have degree 2).
            cycles = []
            guard = 0
            max_guard = len(edges) * 4 + 16
            while remaining and guard < max_guard:
                guard += 1
                start_edge = next(iter(remaining))
                v0 = start_edge.verts[0]
                stack_v = [v0]
                stack_e = []
                cur = v0
                progressed = False
                while True:
                    nxt_edge = nxt_vert = None
                    for e, other in adj.get(cur, []):
                        if e in remaining:
                            nxt_edge, nxt_vert = e, other
                            break
                    if nxt_edge is None:
                        break
                    remaining.discard(nxt_edge)
                    progressed = True
                    if nxt_vert in stack_v:
                        idx = stack_v.index(nxt_vert)
                        cyc = stack_e[idx:] + [nxt_edge]
                        if len(cyc) >= 3:
                            cycles.append(cyc)
                        stack_v = stack_v[:idx + 1]
                        stack_e = stack_e[:idx]
                        cur = nxt_vert
                    else:
                        stack_v.append(nxt_vert)
                        stack_e.append(nxt_edge)
                        cur = nxt_vert
                if not progressed:
                    remaining.discard(start_edge)

            leftover = len(remaining)
            return cycles, open_chains, leftover

        def _loop_planar_extent_local(loop_edges, n_plane):
            """Return (extent, avg_coord) of a loop's spread along n_plane."""
            verts = set()
            for e in loop_edges:
                verts.add(e.verts[0]); verts.add(e.verts[1])
            vals = [v.co.dot(n_plane) for v in verts]
            return (max(vals) - min(vals)), (sum(vals) / len(vals))

        def _perimeter_local(loop_edges):
            p = 0.0
            for e in loop_edges:
                v0, v1 = e.verts
                p += (v0.co - v1.co).length
            return p


        n_plane = split_no
        eps_plane = _diag_eps(obj, k=5e-6, min_eps=5e-7)
        eps_plane_loop = _diag_eps(obj, k=8e-6, min_eps=8e-7)

        cycles, open_chains, leftover = _decompose_all_into_loops_and_chains_local(cand)
        print(f"[SnapSplit DEBUG] global decomposition: {len(cycles)} closed cycle(s), "
              f"{len(open_chains)} open chain(s), leftover edges={leftover}")
        if leftover:
            print(f"[SnapSplit DEBUG] WARNING: {leftover} boundary edge(s) could not be "
                  f"resolved into cycles or chains (decomposition guard limit hit)")

        # Open chains can never be capped (no closed loop exists) -- report
        # explicitly instead of letting them vanish silently. This is the
        # expected outcome for a mesh feature like Suzanne's nose hole that
        # the split plane happens to cut through.
        for ci, chain in enumerate(open_chains):
            verts = set()
            for e in chain:
                verts.add(e.verts[0]); verts.add(e.verts[1])
            ends = [v for v in verts if sum(1 for e in chain if v in e.verts) == 1]
            per = _perimeter_local(chain)
            print(f"[SnapSplit][INFO] open boundary chain #{ci}: {len(chain)} edge(s), "
                  f"length~{per:.4f} -- cannot form a closed loop, leaving open "
                  f"(likely rim of a pre-existing mesh opening, e.g. an un-capped "
                  f"nose hole or drain)")
            for v in ends:
                print(f"[SnapSplit][INFO]   chain endpoint at {tuple(round(c, 6) for c in v.co)}")

        # Classify closed cycles: planar (real cut-plane loop) vs. wandering
        # non-planar (closed ring that drifts off the cut plane, e.g. a
        # slanted rim of a wall opening) -- the latter is excluded from
        # capping with an explicit INFO message instead of a silent drop.
        planar_loops = []
        for cy in cycles:
            extent, avg_coord = _loop_planar_extent_local(cy, n_plane)
            per = _perimeter_local(cy)
            if extent <= eps_plane_loop:
                planar_loops.append({'edges': cy, 'coord': avg_coord})
                print(f"[SnapSplit DEBUG] closed cycle: {len(cy)} edge(s), perimeter={per:.4f}, "
                      f"extent along axis={extent:.6g} -> PLANAR, kept for capping")
            else:
                print(f"[SnapSplit][INFO] closed cycle: {len(cy)} edge(s), perimeter={per:.4f}, "
                      f"extent along axis={extent:.6g} (threshold={eps_plane_loop:.6g}) -> "
                      f"NON-PLANAR wandering ring, excluding from capping "
                      f"(likely rim of a pre-existing wall opening rather than the cut plane)")

        if not planar_loops:
            print("[SnapSplit DEBUG] no planar closed loops found -> nothing to cap")
            return False

        # Group surviving planar loops into cut-plane buckets by position,
        # for the existing single-loop / multi-loop (cavity ring) fill logic.
        planar_loops.sort(key=lambda d: d['coord'])
        buckets = []
        for pl in planar_loops:
            matched = False
            for b in buckets:
                if abs(pl['coord'] - b['v']) <= eps_plane:
                    b['loops'].append(pl['edges'])
                    b['v'] = (b['v'] * 0.9) + (pl['coord'] * 0.1)
                    matched = True
                    break
            if not matched:
                buckets.append({'v': pl['coord'], 'loops': [pl['edges']]})
        print(f"[SnapSplit DEBUG] {len(buckets)} cut-plane bucket(s) from planar loops "
              f"(eps_plane={eps_plane:.6g}):")
        for i, b in enumerate(buckets):
            print(f"[SnapSplit DEBUG]   bucket[{i}] coord~{b['v']:.5f} loop_count={len(b['loops'])}")

        for bi, bucket in enumerate(buckets):
            loops = bucket['loops']
            print(f"[SnapSplit DEBUG] -- filling bucket[{bi}]: {len(loops)} loop(s) --")

            # Group loops into 'outer + holes' by 2D nesting (None -> legacy behaviour)
            groups = _group_loops_by_nesting(loops, ax)
            if groups is None:
                print("[SnapSplit DEBUG]   nesting analysis failed -> legacy single group")
                groups = [{'edges': [e for lp in loops for e in lp],
                           'n_holes': len(loops) - 1,
                           'expected_area': None}]

            for gi, grp in enumerate(groups):
                g_edges = grp['edges']

                if grp['n_holes'] == 0:
                    print(f"[SnapSplit DEBUG]   group {gi}: plain loop -> BMesh fill (N-gon first)")
                    # No selection needed anymore: the edges are passed to the BMesh op directly
                    did = _fill_edges_bmesh(bm, g_edges, prefer_ngon=True, normal=n_plane)
                    bmesh.update_edit_mesh(obj.data)

                else:
                    print(f"[SnapSplit DEBUG]   group {gi}: outer loop + {grp['n_holes']} hole(s) "
                          f"-> verified triangle_fill")
                    did = _fill_nested_group_bmesh(bm, g_edges, n_plane,
                                                   grp['n_holes'], grp['expected_area'])
                    bmesh.update_edit_mesh(obj.data)
                print(f"[SnapSplit DEBUG]   group {gi} fill result: {did}")
                any_ok = any_ok or did

        if any_ok:
            # Recalculate normals directly on the edit BMesh
            # (replaces select_all + normals_make_consistent operators).
            try:
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
                bmesh.update_edit_mesh(obj.data)
            except Exception as ex:
                print(f"[SnapSplit DEBUG] recalc_face_normals raised: {ex}")

        return any_ok

    except Exception as ex:
        print(f"[SnapSplit DEBUG] EXCEPTION inside cap_single_object_hollow_style: {ex}")
        raise
    finally:
        # Safety net: guarantee we always leave edit mode, even if an
        # exception occurs above, to avoid corrupting the operator context
        # for subsequent bpy.ops calls (observed crash in select_all).
        _leave_edit_mode()
        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass
        print(f"[SnapSplit DEBUG] ---- cap_single_object_hollow_style: {obj.name} DONE, any_ok={any_ok} ----")

# ---------------------------
# Auto "Apply Rotation & Scale" before the planar split
# ---------------------------

def apply_rotation_and_scale(obj):
    """Bake rotation and scale of obj into its mesh data. Location is NOT applied.

    The result is the same as Ctrl+A > Rotation & Scale: the object keeps its world
    position and shape, but its local axes become the world axes. Cut planes,
    capping and seam detection (all world-axis based) then work in the same space.

    Handles parents (detached while keeping the world matrix), children (world
    matrix restored), shared mesh data (own copy is made), shape keys and
    mirrored (negative determinant) transforms.
    Returns True if the object was modified, False if nothing was done or the
    object could not be baked safely.
    """
    from mathutils import Matrix  # local import: no change to the module header needed

    if obj is None or obj.type != 'MESH' or obj.data is None:
        return False
    # Mesh.transform() cannot be used while the mesh is in Edit Mode
    if obj.mode != 'OBJECT':
        return False

    # Make sure matrix_world is up to date before reading it
    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    M = obj.matrix_world.copy()
    rs = M.to_3x3()  # rotation + scale (+ parent contribution), without translation

    # Nothing to do if the object space is already aligned with the world axes
    dev = max(abs(rs[i][j] - (1.0 if i == j else 0.0)) for i in range(3) for j in range(3))
    if dev < 1e-6:
        return False

    # Remember the world matrices of children so they do not move afterwards
    children = [(c, c.matrix_world.copy()) for c in obj.children]

    # Detach from the parent while keeping the world transform
    if obj.parent is not None:
        obj.parent = None
        obj.matrix_world = M

    # Shared mesh data would change other objects too: give this object its own copy
    if obj.data.users > 1:
        obj.data = obj.data.copy()

    if rs.determinant() < 0.0:
        # DOCUMENTED FALLBACK (same reason as in _apply_object_scale_if_needed):
        # a mirroring transform flips the winding, so use Blender's own operator.
        # The context override restricts the operator to this single object.
        try:
            with bpy.context.temp_override(active_object=obj, object=obj,
                                           selected_objects=[obj],
                                           selected_editable_objects=[obj]):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        except Exception as ex:
            print(f"[SnapSplit] transform_apply fallback failed: {ex}")
            return False
    else:
        has_keys = getattr(obj.data, "shape_keys", None) is not None
        m4 = rs.to_4x4()
        try:
            # Transform shape keys together with the base mesh
            obj.data.transform(m4, shape_keys=True)
        except TypeError:
            # 'shape_keys' argument not available: only safe without shape keys
            if has_keys:
                print("[SnapSplit] Object has shape keys; transform not applied.")
                return False
            obj.data.transform(m4)
        obj.data.update()
        # Keep only the world position on the object (rotation 0, scale 1)
        obj.matrix_world = Matrix.Translation(M.translation)

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    # Restore the world matrices of the children
    for c, mw in children:
        try:
            c.matrix_world = mw
        except Exception:
            pass
    return True



class SNAP_OT_planar_split(Operator):
    """Split the active mesh into multiple parts along a selected axis, with optional auto-capping."""
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute the split operation and optionally cap seams depending on settings."""
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        'Please select a mesh object.')
            return {'CANCELLED'}

        # Normalize hollow and record used_hollow flag
        used_hollow = False

        try:
            obj, used_hollow = robust_prepare_hollow(obj, operator=self)
            obj.data.validate(); obj.data.update()
        except Exception as e:
            print(f"[SnapSplit] Hollow prepare failed: {e}")

        props = context.scene.snapsplit
        # Auto-cap toggle (reads from scene props)
        auto_cap = bool(getattr(props, "cap_seams_during_split", False))

        axis = props.split_axis
        count = max(2, int(props.parts_count))
        if count >= 12:
            self.report({'INFO'}, _trf('Splitting into many parts can take a while on dense meshes...'))

        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()
                # Apply rotation and scale AFTER the cuts were computed (so they match the orange
        # preview exactly) and BEFORE the split (so mesh space == world space).
        # The cut planes are world coordinates and the object keeps its world position
        # and shape, so the cuts stay valid. A failure must never block the split.
        try:
            if apply_rotation_and_scale(obj):
                report_user(self, 'INFO',
                            'Rotation and scale were applied before splitting.')
        except Exception as ex:
            print(f"[SnapSplit] Auto apply rotation/scale failed: {ex}")


        cuts = create_cut_data_with_offset(obj, axis, count, global_offset_scene=offset_scene)

        parts = apply_bmesh_split_sequence(obj, axis, count, cuts_override=cuts, operator=self)

        # Auto-cap after splitting if enabled
        if auto_cap and parts:
            capped_cnt = 0
            # NOTE: always use the ring-aware capping algorithm now, regardless
            # of used_hollow. Reliably detecting "this object has a hollow
            # cavity" up front is not feasible for arbitrary user setups (e.g.
            # a manually applied Boolean modifier using an unrelated source
            # object, such as a Sphere carving a cavity into a Cube) -- neither
            # _try_apply_hollow_modifier's Solidify/named-NODES check nor
            # _find_paired_inner_object_for's name-matching heuristic can
            # detect that case. cap_single_object_hollow_style() now correctly
            # handles both plain solid cross-sections (single loop per plane)
            # and cavity rings (two loops per plane), so it is safe and
            # correct to use unconditionally, replacing the previous
            # used_hollow-gated fallback to _cap_single_object_simple_fill()
            # (which could not distinguish outer from inner loops and sealed
            # cavities shut).
            for p in parts:
                try:
                    if cap_single_object_hollow_style(p):
                        capped_cnt += 1
                except Exception:
                    pass

            if capped_cnt == 0:
                report_user(self, 'WARNING',
                            'Auto-cap during split did not find valid loops to fill.')
            else:
                msg = _trf("Auto-capped seams on {n} part(s).", n=capped_cnt)
                report_user(self, 'INFO', msg)


        if len(parts) < count:
            msg = _trf("Fewer parts created than expected ({have} < {want}).",
                       have=len(parts), want=count)
            report_user(self, 'WARNING', msg)
        else:
            msg = _trf("{n} parts created.", n=len(parts))
            report_user(self, 'INFO', msg)

        # ---------------------------
        # Route results into per-job collections (visible Parts, hidden Helpers)
        # ---------------------------

        parts_job_coll, helpers_job_coll = _ensure_job_collections(obj.name)

        # Build sets to separate final vs intermediate
        final_parts_set = set(parts)

        # Heuristic: any mesh whose name starts with the source name and isn't a final is considered intermediate
        candidates = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(obj.name)]
        intermediates = [o for o in candidates if o not in final_parts_set]

        # 1) Link only the final parts to the visible Parts job collection
        # (RNA-based deselect instead of bpy.ops.object.select_all)
        _deselect_all_objects()
        for p in parts:
            # Unlink from any other collections to keep Outliner clean
            try:
                for c in list(p.users_collection):
                    try:
                        c.objects.unlink(p)
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                parts_job_coll.objects.link(p)
            except Exception:
                pass
            p.hide_set(False)
            p.select_set(True)

        if parts:
            bpy.context.view_layer.objects.active = parts[0]

        # 2) Move preview planes (if any left) to Helpers and hide
        try:
            preview_objs = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]
            _move_objs_to_collection(preview_objs, helpers_job_coll, hide=True, unlink_first=True)
        except Exception:
            pass

        # 3) Move intermediate artifacts to Helpers and hide
        try:
            _move_objs_to_collection(intermediates, helpers_job_coll, hide=True, unlink_first=True)
        except Exception:
            pass

        # 4) Move service objects (e.g., cutters) to Helpers and optionally remove now-empty service collections
        for svc_name in ("_SnapSplit_Cutters",):
            try:
                c = bpy.data.collections.get(svc_name)
                if c:
                    _move_objs_to_collection(list(c.objects), helpers_job_coll, hide=True, unlink_first=True)
                    # Optionally remove the empty service collection to reduce clutter
                    if len(c.objects) == 0:
                        for sc in bpy.data.scenes:
                            try:
                                if c in sc.collection.children:
                                    sc.collection.children.unlink(c)
                            except Exception:
                                pass
                        try:
                            bpy.data.collections.remove(c)
                        except Exception:
                            pass
            except Exception:
                pass

        # Keep your preview system cleanup (safe)
        try:
            update_split_preview_plane(context)
        except Exception:
            pass
        try:
            _disable_split_preview_and_cleanup(context)
        except Exception:
            pass

        return {'FINISHED'}

# ---------------------------
# Cap seams now – precise outer/inner loop detection (manual)
# ---------------------------

def _loops_from_edges_connected(edges):
    """Return connected components of edges as lists (for loop detection)."""
    rem = set(edges)
    comps = []
    while rem:
        start = rem.pop()
        comp = {start}
        stack = [start]
        while stack:
            e = stack.pop()
            for v in e.verts:
                for e2 in v.link_edges:
                    if e2 in rem:
                        rem.remove(e2)
                        comp.add(e2)
                        stack.append(e2)
        if len(comp) >= 3:
            comps.append(list(comp))
    return comps

def _perimeter_of_edges(loop):
    """Return approximate perimeter of a given edge loop list."""
    p = 0.0
    for e in loop:
        v0, v1 = e.verts
        p += (v0.co - v1.co).length
    return p

# ---------------------------
# Conservative pure-BMesh edge-loop walker (replaces bpy.ops.mesh.loop_multi_select)
# ---------------------------

def _next_edge_in_loop(edge, vert, boundary_mode):
    """Return the next edge when walking an edge loop through 'vert', or None if ambiguous.

    Rules (deliberately strict; any ambiguity returns None):
      - boundary_mode (seed edge is a boundary edge): the next edge is the ONLY
        other boundary edge at 'vert'. More than one or none -> ambiguous.
      - interior mode: 'vert' must have exactly 4 edges and the current edge must
        have exactly 2 faces. The next edge is the single edge at 'vert' that shares
        no face with the current edge (the "opposite" edge in a quad grid).
    """
    if boundary_mode:
        cands = [e for e in vert.link_edges if e != edge and e.is_boundary]
        return cands[0] if len(cands) == 1 else None

    if len(vert.link_edges) != 4:
        return None
    edge_faces = set(edge.link_faces)
    if len(edge_faces) != 2:
        return None
    cands = [e for e in vert.link_edges
             if e != edge and not (edge_faces & set(e.link_faces))]
    return cands[0] if len(cands) == 1 else None

def _walk_edge_loop_closed(seed_edge, max_steps):
    """Walk an edge loop through 'seed_edge' and return its edges ONLY if it is a closed cycle.

    Returns a list of BMEdge objects forming a closed loop, or None when the loop
    cannot be proven closed (open chain, ambiguous vertex, revisited edge, step
    limit reached). The walker never modifies the mesh or the selection.
    """
    try:
        if seed_edge is None or not seed_edge.is_valid:
            return None

        boundary_mode = bool(seed_edge.is_boundary)
        start_vert = seed_edge.verts[0]
        cur_vert = seed_edge.verts[1]
        cur_edge = seed_edge

        loop = [seed_edge]
        visited = {seed_edge}

        for _ in range(max(4, int(max_steps))):
            nxt = _next_edge_in_loop(cur_edge, cur_vert, boundary_mode)
            if nxt is None:
                return None
            if nxt == seed_edge:
                # Closed only if we came back through the start vertex of the seed edge
                return loop if (cur_vert == start_vert and len(loop) >= 3) else None
            if nxt in visited:
                # Revisiting an edge that is not the seed -> pinch/figure-eight, reject
                return None
            loop.append(nxt)
            visited.add(nxt)
            cur_vert = nxt.other_vert(cur_vert)
            cur_edge = nxt
        return None
    except Exception:
        return None


class SNAP_OT_cap_open_seams_now(Operator):
    """Fill between exactly two split edge loops (outer+inner) per plane; prefers seed edges if present."""
    bl_idname = "snapsplit.cap_open_seams_now"
    bl_label = "Cap seams now"
    bl_description = 'Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred.'
    bl_options = {'REGISTER', 'UNDO'}

    only_selected: bpy.props.BoolProperty(
        name='Only selected objects',
        default=True
    )
    max_planes: bpy.props.IntProperty(
        name='Max planes',
        description='0 = all planes per object, 1 = only largest',
        default=0, min=0, soft_max=12
    )
    select_only: bpy.props.BoolProperty(
        name='Select only (no fill)',
        default=False
    )
    require_two_seeds: bpy.props.BoolProperty(
        name='Require exactly two seed edges',
        description='If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection).',
        default=False
    )

    def _plane_axis_for_object(self, obj):
        """Return the split axis for the given object from scene props."""
        props = getattr(bpy.context.scene, "snapsplit", None)
        return props.split_axis if props else "Z"

    def _seeds_exact_two_edges(self, bm):
        """Return the selected two edges if exactly two are selected, else None."""
        sel_edges = [e for e in bm.edges if e.select]
        return sel_edges if len(sel_edges) == 2 else None

    def _expand_edge_to_full_loop_ops(self, obj, bm, edge):
        """DOCUMENTED FALLBACK: expand an edge to a loop via bpy.ops.mesh.loop_multi_select.

        Only used when the pure-BMesh walker cannot prove a closed cycle.
        Blender's C edge-loop walker has no public Python equivalent, so this is
        the single remaining operator-based loop selection in SnapSplit.
        This fallback changes the BMesh selection (as the original code did).
        """
        for e in bm.edges:
            e.select = False
        edge.select = True
        bmesh.update_edit_mesh(obj.data)
        try:
            bpy.ops.mesh.loop_multi_select(ring=False)
        except Exception:
            pass
        return [e for e in bm.edges if e.select]

    def _expand_edge_to_full_loop(self, obj, bm, edge):
        """Expand a selected edge to a full edge loop and return the loop edges.

        Step 1: pure-BMesh walker (no operator, no selection change).
        Step 2: if no closed cycle could be proven, fall back to the operator
                (only if _ALLOW_OPS_LOOP_FALLBACK is True).
        """
        try:
            bm.edges.ensure_lookup_table()
            walked = _walk_edge_loop_closed(edge, max_steps=len(bm.edges) + 1)
        except Exception:
            walked = None
        if walked:
            return walked

        if _ALLOW_OPS_LOOP_FALLBACK:
            print("[SnapSplit DEBUG] edge-loop walker found no closed cycle -> "
                  "falling back to bpy.ops.mesh.loop_multi_select for this seed")
            return self._expand_edge_to_full_loop_ops(obj, bm, edge)

        # Fallback disabled: return only the seed edge (will fail the cyclic check)
        return [edge]

    def _loop_is_cyclic_degree2(self, loop_edges):
        """Check if edges form a simple cycle where every vertex has degree 2."""
        count = {}
        for e in loop_edges:
            for v in e.verts:
                count[v] = count.get(v, 0) + 1
        return all(c == 2 for c in count.values()) and len(loop_edges) >= 3

    def _fill_like_altf(self, obj, bm, edges):
        """Fill the given loops like Mesh > Fill (Alt+F) using BMesh only (no operator, no selection)."""
        ok = _fill_edges_bmesh(bm, edges, prefer_ngon=False)
        if ok:
            bmesh.update_edit_mesh(obj.data)
        return ok


    def _cluster_split_ring_edges(self, obj, bm, plane_axis):
        """Cluster boundary edges into groups per split plane along the given axis."""
        ax = axis_index_for(plane_axis)
        axis_vecs = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))
        split_no = axis_vecs[ax].normalized()

        eps_plane = _diag_eps(obj, k=5e-6, min_eps=5e-7)
        eps_dir = 0.12

        cand = []
        for e in bm.edges:
            if not e.is_boundary:
                continue
            d = (e.verts[1].co - e.verts[0].co)
            if d.length_squared == 0.0:
                continue
            d.normalize()
            if abs(d.dot(split_no)) > eps_dir:
                continue
            cand.append(e)

        if not cand:
            return []

        mvals = [(e, (0.5 * (e.verts[0].co + e.verts[1].co)).dot(split_no)) for e in cand]
        mvals.sort(key=lambda t: t[1])

        planes = []
        for e, val in mvals:
            matched = False
            for pl in planes:
                if abs(val - pl['v']) <= eps_plane:
                    pl['edges'].append(e)
                    pl['v'] = (pl['v'] * 0.9) + (val * 0.1)
                    matched = True
                    break
            if not matched:
                planes.append({'v': val, 'edges': [e]})

        planes.sort(key=lambda d: len(d['edges']), reverse=True)
        return [pl['edges'] for pl in planes]

    def _cap_single_object(self, obj, max_planes=0, select_only=False) -> bool:
        """Run the capping routine on a single mesh object, optionally only selecting loops."""
        _enter_edit_mode_edges(obj)
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

        # 1) Strict two-edge seeds
        if self.require_two_seeds:
            seeds = self._seeds_exact_two_edges(bm)
            if seeds:
                loop_a = self._expand_edge_to_full_loop(obj, bm, seeds[0])
                loop_b = self._expand_edge_to_full_loop(obj, bm, seeds[1])
                if self._loop_is_cyclic_degree2(loop_a) and self._loop_is_cyclic_degree2(loop_b):
                    for e in bm.edges: e.select = False
                    for e in loop_a + loop_b: e.select = True
                    bmesh.update_edit_mesh(obj.data)
                    if not select_only:
                        ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                        _leave_edit_mode()

                        if ok:
                            # Recalculate normals via BMesh (no Edit Mode round trip)
                            _recalc_normals_outside(obj)
                        return ok
                    else:
                        _leave_edit_mode()
                        return True
            _leave_edit_mode()
            return False

        # 2) Seeds preferred (>=2 edges): take two largest loops
        sel_edges = [e for e in bm.edges if e.select]
        if len(sel_edges) >= 2:
            loops = []
            seen = set()
            for e in sel_edges[:4]:
                if e in seen: continue
                loops.append(self._expand_edge_to_full_loop(obj, bm, e)); seen.add(e)
            loops = [lp for lp in loops if self._loop_is_cyclic_degree2(lp)]
            loops.sort(key=lambda lp: _perimeter_of_edges(lp), reverse=True)
            if len(loops) >= 2:
                loop_a, loop_b = loops[0], loops[1]
                for e in bm.edges: e.select = False
                for e in loop_a + loop_b: e.select = True
                bmesh.update_edit_mesh(obj.data)
                if not select_only:
                    ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                    _leave_edit_mode()

                    if ok:
                        # Recalculate normals via BMesh (no Edit Mode round trip)
                        _recalc_normals_outside(obj)
                    return ok
                else:
                    _leave_edit_mode()
                    return True

        # 3) Automatic detection – group true split rings per plane
        plane_axis = self._plane_axis_for_object(obj)
        ring_groups = self._cluster_split_ring_edges(obj, bm, plane_axis)
        if not ring_groups:
            _leave_edit_mode()
            return False

        ax = axis_index_for(plane_axis)
        n_plane = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))[ax].normalized()
        eps_plane_loop = _diag_eps(obj, k=8e-6, min_eps=8e-7)

        processed = 0
        all_ok = True
        any_selected = False

        for edges_on_plane in ring_groups:
            if max_planes and processed >= max_planes:
                break

            # Build connected edge sets (loop candidates) and keep only degree-2 cyclic loops
            comps = _loops_from_edges_connected(edges_on_plane)
            comps = [c for c in comps if self._loop_is_cyclic_degree2(c)]

            # Single-loop quick path (solid caps) BEFORE planarity tests (still fine for cubes)
            if len(comps) == 1:
                loop_a = comps[0]
                for e in bm.edges:
                    e.select = False
                for e in loop_a:
                    e.select = True
                bmesh.update_edit_mesh(obj.data)

                did = False
                if not select_only:
                    # N-gon first (like edge_face_add), then triangle fill; no operators
                    did = _fill_edges_bmesh(bm, loop_a, prefer_ngon=True, normal=n_plane)
                    if did:
                        bmesh.update_edit_mesh(obj.data)
                else:
                    did = True  # selection-only mode


                any_selected = True
                all_ok = all_ok and did
                processed += 1
                continue

            if len(comps) < 2:
                all_ok = False
                continue

            # Planarity filter
            mids = [(0.5 * (e.verts[0].co + e.verts[1].co)) for e in edges_on_plane]
            p_plane = sum(mids, Vector((0,0,0))) * (1.0 / max(1, len(mids)))

            comps = [c for c in comps if max(abs((v.co - p_plane).dot(n_plane)) for e in c for v in e.verts) <= eps_plane_loop]
            if len(comps) < 2:
                all_ok = False
                continue

            comps.sort(key=lambda lp: _perimeter_of_edges(lp), reverse=True)

            i = 0
            plane_ok = True
            while i + 1 < len(comps):
                loop_a, loop_b = comps[i], comps[i+1]
                for e in bm.edges: e.select = False
                for e in loop_a + loop_b: e.select = True
                bmesh.update_edit_mesh(obj.data)
                any_selected = True
                if not select_only:
                    ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                    plane_ok = plane_ok and ok

                i += 2

            all_ok = all_ok and plane_ok
            processed += 1

        _leave_edit_mode()
        if not select_only and all_ok and processed > 0:
            # Recalculate normals via BMesh (no Edit Mode round trip)
            _recalc_normals_outside(obj)

        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass

        return (all_ok and processed > 0) or (select_only and any_selected)

    def execute(self, context):
        """Execute capping for selected targets or the parts collection."""
        if self.only_selected:
            targets = [o for o in context.selected_objects if o.type == 'MESH']
        else:
            parts_coll = bpy.data.collections.get("SnapSplit_Parts")
            targets = [o for o in (list(parts_coll.objects) if parts_coll else []) if o and o.type == 'MESH']

        if not targets:
            report_user(self, 'ERROR',
                        'No mesh objects to cap. Select split parts or use the parts collection.')
            return {'CANCELLED'}

        success = 0
        for obj in targets:
            try:
                if self._cap_single_object(obj, max_planes=self.max_planes, select_only=self.select_only):
                    success += 1
            except Exception as e:
                _leave_edit_mode()
                # Fill the {name}/{err} placeholders AFTER the translation lookup
                msg = _trf("Processing failed on '{name}': {err}",
                           name=obj.name, err=str(e))
                report_user(self, 'WARNING', msg)

        if success == 0:
            if self.select_only:
                report_user(self, 'WARNING',
                            'Could not determine split edge loops to select.')
            else:
                report_user(self, 'WARNING',
                            'Could not determine and fill split edge loops.')
            return {'CANCELLED'}

        # Fill the {n} placeholder AFTER the translation lookup
        if self.select_only:
            msg = _trf("Selected split edge loops on {n} object(s).", n=success)
        else:
            msg = _trf("Capped seams on {n} object(s).", n=success)
        report_user(self, 'INFO', msg)
        return {'FINISHED'}


# ---------------------------
# Registration
# ---------------------------

classes = (
    SNAP_OT_adjust_split_axis,
    SNAP_OT_planar_split,
    SNAP_OT_cap_open_seams_now,
)

def register():
    """Register operators. The depsgraph handler is NOT added unconditionally anymore."""
    # Labels and descriptions are plain class attributes; Blender translates them itself.
    for c in classes:
        bpy.utils.register_class(c)


    # Drop stale handlers first (e.g. left over from a hot reload), then install the
    # one-shot file-load check and attach the depsgraph handler only if a preview is on.
    _remove_handlers_named(bpy.app.handlers.depsgraph_update_post, _DEPSGRAPH_HANDLER_NAME)
    _remove_handlers_named(bpy.app.handlers.load_post, _LOAD_HANDLER_NAME)
    bpy.app.handlers.load_post.append(_snapsplit_load_post)
    sync_depsgraph_handler()


def unregister():
    """Unregister operators and make sure no SnapSplit handler stays behind."""
    global _last_preview_active_obj, _last_connector_preview_selection_key
    # Never leave X-Ray switched on when the add-on is disabled
    try:
        from .utils import xray_release
        xray_release(None)
    except Exception:
        pass
    _remove_handlers_named(bpy.app.handlers.depsgraph_update_post, _DEPSGRAPH_HANDLER_NAME)
    _remove_handlers_named(bpy.app.handlers.load_post, _LOAD_HANDLER_NAME)
    _last_preview_active_obj = None
    _last_connector_preview_selection_key = None

    for c in reversed(classes):
        bpy.utils.unregister_class(c)
```

---

### prefs.py

```py
'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''

# prefs.py

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty, FloatProperty

class SNAPADDON_Preferences(AddonPreferences):
    """Add-on preferences for SnapSplit."""
    bl_idname = __package__  # "snapsplit"

    default_profile: StringProperty(
        name="Default Profile",
        default="PLA",
        description="Default material/printer profile",
    )
    create_export_collection: BoolProperty(
        name="Create export collection",
        default=True,
        description="Create a collection for parts ready to export",
    )

    def draw(self, context):
        """Draw the add-on preferences UI."""
        layout = self.layout
        layout.prop(self, "default_profile")
        layout.prop(self, "create_export_collection")

classes = (SNAPADDON_Preferences,)

def register():
    """Register add-on preferences."""
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    """Unregister add-on preferences."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
```

---

### profiles.py

```py
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# profiles.py

import math
import bpy
from bpy.props import (
    EnumProperty,
    FloatProperty,
    PointerProperty,
    IntProperty,
    BoolProperty,
)
from bpy.types import PropertyGroup

from .utils import unit_mm, mm_to_scene, scene_to_mm, _trf

# ---------------------------
# Material profiles (tolerance per side, in mm)
# ---------------------------

MATERIAL_PROFILES = {
    "PLA": 0.20,
    "PETG": 0.30,
    "ABS": 0.25,
    "ASA": 0.25,
    "TPU": 0.35,
    "SLA": 0.10,
}


def _snapsplit_update_preview(self, context):
    """Property update callback to refresh or clear split preview planes."""
    try:
        from . import ops_split
        ops_split.update_split_preview_plane(context)
    except Exception:
        # Fail silently to not break UI interactions if preview operator is unavailable
        pass


def _snapsplit_update_connector_preview(self, context):
    """Property update callback to refresh or clear the connector placement live preview.

    This is fully independent from the split-plane preview above. The called
    function itself checks the 'connector_live_preview' toggle and the current
    selection/distribution mode, and performs cleanup when preview is not
    applicable. Kept in a try/except so UI interactions never break, even if
    the preview builder raises under unusual context states (e.g. during
    file load or when running from a background context).
    """
    try:
        from . import ops_connectors
        ops_connectors.update_connector_placement_preview(context)
    except Exception:
        # Fail silently to not break UI interactions if the preview function is unavailable
        pass

def _snapsplit_update_show_split_preview(self, context):
    """Update callback of 'show_split_preview': X-Ray, refresh the preview, sync the depsgraph handler."""
    try:
        # X-Ray on while the cut preview is shown, so the planes are visible inside solid
        # objects; restored when the preview is switched off (also via cleanup code).
        try:
            from .utils import xray_acquire, xray_release
            if bool(getattr(self, "show_split_preview", False)):
                xray_acquire(context, "split_preview")
            else:
                xray_release("split_preview")
        except Exception:
            pass
        _snapsplit_update_preview(self, context)
    finally:
        try:
            from . import ops_split
            ops_split.sync_depsgraph_handler()
        except Exception:
            # Never break UI interaction because of handler bookkeeping
            pass


def _snapsplit_update_connector_live_preview(self, context):
    """Update callback of 'connector_live_preview': X-Ray, refresh the preview, sync the handler."""
    try:
        # Same X-Ray handling as the cut preview, with its own reason so both can run together
        try:
            from .utils import xray_acquire, xray_release
            if bool(getattr(self, "connector_live_preview", False)):
                xray_acquire(context, "connector_preview")
            else:
                xray_release("connector_preview")
        except Exception:
            pass
        _snapsplit_update_connector_preview(self, context)
    finally:
        try:
            from . import ops_split
            ops_split.sync_depsgraph_handler()
        except Exception:
            pass



def _snapsplit_update_connector_type(self, context):
    """Property update callback for connector_type.

    Besides refreshing the live preview (same as the generic connector
    property callback), this resets the shared 'dovetail_span_axis' enum
    to the sensible default for the newly selected connector type, since
    that single property is reused across DOVETAIL, SNAP_DOVETAIL and
    CUSTOM but each type has a different practical default:
      - DOVETAIL / SNAP_DOVETAIL -> "AUTO" (auto-stretch + trim, as before
        this property existed for Custom Connector)
      - CUSTOM -> "NONE" (a picked mesh usually has an intentional fixed
        size; auto-stretching an arbitrary shape is rarely wanted)
      - all other types (CYL_PIN, RECT_TENON, SNAP_PIN, SNAP_TENON) do not
        expose Span Axis in the UI at all, so the property is left as-is.

    This intentionally overwrites any value the user set for the previous
    type on every switch (confirmed behavior), rather than remembering a
    per-type value, since the three types are geometrically unrelated and
    a carried-over value would usually be meaningless for the new type.
    """
    try:
        ctype = str(getattr(self, "connector_type", ""))
        if ctype in {"DOVETAIL", "SNAP_DOVETAIL"}:
            if getattr(self, "dovetail_span_axis", None) != "AUTO":
                self.dovetail_span_axis = "AUTO"
        elif ctype == "CUSTOM":
            if getattr(self, "dovetail_span_axis", None) != "NONE":
                self.dovetail_span_axis = "NONE"
    except Exception:
        # Never break the connector_type dropdown itself if the span-axis
        # property is unavailable for any reason (e.g. older scene data).
        pass

    # Preserve the original behavior: still refresh/clear the live preview.
    _snapsplit_update_connector_preview(self, context)


def _suggest_pin_segments_from_diameter(d_mm: float) -> int:
    """
    Return a heuristic segment count for cylindrical pins from diameter in mm.
    Aims for visually round pins suitable for 3D printing without heavy meshes.
    """
    if d_mm <= 0:
        return 16
    base = int(round(math.pi * d_mm / 1.8))
    lo, hi = 12, 64
    if d_mm < 3.0:
        lo = 16
    return max(lo, min(hi, base))


def _mat_item_desc(key: str, val: float) -> str:
    """
    Build a localized tooltip text for a material profile entry.

    Formats the English template with {val} = tolerance value in mm, rounded to 2 decimals.
    """
    # Use _trf to format the template with the tolerance value.
    # val must be passed as a float for proper formatting.
    try:
        return _trf("Recommended tolerance per side: {val:.2f} mm", val=float(val))
    except Exception:
        return f"Recommended tolerance per side: {val:.2f} mm"

def material_tooltip(val):
    """Return a localized tooltip for the material tolerance value.

    Formats the English template with {val} = tolerance value in mm, rounded to 2 decimals.
    """
    try:
        return _trf("Recommended tolerance per side: {val:.2f} mm", val=float(val))
    except Exception:
        return f"Recommended tolerance per side: {val:.2f} mm"


def _material_items():
    """Return EnumProperty items for material profiles with localized tooltips."""
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

def _poll_custom_connector_object(self, obj):
    """Restrict the Custom Connector object picker to mesh objects only."""
    return obj.type == 'MESH'

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
    """Scene-level settings for segmentation, preview, connectors, tolerances, and alignment."""

    # Split / Preview
    split_offset_mm: FloatProperty(
        name='Split Offset (mm)',
        description='Offset of the cutting plane along the split axis (positive in axis direction)',
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_preview,
    )

    split_axis: EnumProperty(
        name='Split Axis',
        items=[
            ("X", "X", 'Split along X'),
            ("Y", "Y", 'Split along Y'),
            ("Z", "Z", 'Split along Z'),
        ],
        default="Z",
        update=_snapsplit_update_preview,
    )

    show_split_preview: BoolProperty(
        name='Show split preview',
        description='Show temporary orange planes at planned cut positions',
        default=False,
        update=_snapsplit_update_show_split_preview,      # was: _snapsplit_update_preview
    )

    parts_count: IntProperty(
        name='Number of Parts',
        default=2,
        min=2,
        max=64,
        description='Number of desired segments (cut planes = parts - 1)',
        update=_snapsplit_update_preview,
    )

    # Performance/Workflow: Cap seams automatically during split
    cap_seams_during_split: BoolProperty(
        name='Cap seams during split',
        description='Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime.',
        default=True,
    )

    # Connections
    connector_type: EnumProperty(
        name='Connector Type',
        items=[
            ("CYL_PIN", 'Cylinder Pin', 'Dowel pin + socket'),
            ("RECT_TENON", 'Rectangular Tenon', 'Anti-rotation joint'),
            ("DOVETAIL", 'Dovetail', 'Tapered wedge connector'),
            ("SNAP_PIN", 'Snap Pin', 'Connector with snap spheres'),
            ("SNAP_TENON", 'Snap Tenon', 'Rectangular tenon with snap spheres'),
            ("SNAP_DOVETAIL", 'Snap Dovetail', 'Tapered wedge connector with snap spheres'),
            ("CUSTOM", 'Custom Connector', 'Use another mesh object from the scene as connector shape'),

        ],
        default="CYL_PIN",
        update=_snapsplit_update_connector_type,
    )


    # Placement distribution
    connector_distribution: EnumProperty(
        name='Distribution',
        description='Distribute connectors along a line or a grid across the seam face',
        items=[
            ("LINE", 'Line', 'Place connectors along a line in the seam face'),
            ("GRID", 'Grid', 'Distribute connectors in a grid over the seam face'),
        ],
        default="LINE",
        update=_snapsplit_update_connector_preview,
    )

    connectors_per_seam: IntProperty(
        name='Connectors per Seam',
        default=3,
        min=1,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    connectors_rows: IntProperty(
        name='Rows (GRID)',
        description='Number of rows for grid distribution',
        default=2,
        min=1,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    connector_margin_pct: FloatProperty(
        name='Margin (%)',
        description='Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)',
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Live preview toggle for the LINE/GRID connector distribution.
    # When enabled, non-boolean wireframe placeholders are drawn in the
    # viewport for the currently selected parts, refreshed whenever the
    # selection or any relevant connector property changes.
    connector_live_preview: BoolProperty(
        name='Live Preview',
        description='Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance.',
        default=False,
        # Dedicated callback: switches X-Ray, refreshes the preview and syncs the depsgraph handler
        update=_snapsplit_update_connector_live_preview,
    )

    swap_pin_socket: BoolProperty(
        name='Swap Pin / Socket',
        description='Exchange the roles of the two parts: the pin sits in the other part and the '
                    'socket is cut into this one. Also flips the insertion direction',
        default=False,
        update=_snapsplit_update_connector_preview,
    )



    # Snap options (sphere ring; used by SNAP_PIN / SNAP_TENON)
    snap_spheres_per_side: IntProperty(
        name='Spheres per side',
        description='Number of snap spheres per side/around',
        default=2,
        min=1,
        max=32,
        update=_snapsplit_update_connector_preview,
    )

    snap_sphere_diameter_mm: FloatProperty(
        name='Sphere Diameter (mm)',
        description='Diameter of snap spheres',
        default=2.0,
        min=0.5,
        soft_max=10.0,
        update=_snapsplit_update_connector_preview,
    )

    snap_sphere_protrusion_mm: FloatProperty(
        name='Protrusion (mm)',
        description='How far spheres protrude from side surface',
        default=1.0,
        min=0.0,
        soft_max=5.0,
        update=_snapsplit_update_connector_preview,
    )

    # Pin / Tenon dimensions (mm)
    pin_diameter_mm: FloatProperty(
        name='Pin Diameter (mm)',
        default=5.0,
        min=0.5,
        soft_max=50.0,
        update=_snapsplit_update_connector_preview,
    )

    pin_length_mm: FloatProperty(
        name='Pin Length (mm)',
        default=8.0,
        min=1.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    pin_segments: IntProperty(
        name='Segments',
        description='Cylinder pin radial segments (visual smoothness)',
        default=32,
        min=8,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    tenon_width_mm: FloatProperty(
        name='Tenon Width (mm)',
        default=6.0,
        min=1.0,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    tenon_depth_mm: FloatProperty(
        name='Tenon Depth (mm)',
        default=8.0,
        min=1.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    add_chamfer_mm: FloatProperty(
        name='Chamfer (mm)',
        default=0.3,
        min=0.0,
        soft_max=2.0,
        update=_snapsplit_update_connector_preview,
    )

    # Custom connector (arbitrary mesh object, rescaled to target dimensions)
    custom_connector_object: PointerProperty(
        type=bpy.types.Object,
        name='Select connector object',
        description='Mesh object from this scene used as connector shape. Its local Z axis is treated as the insertion direction; it will be rescaled to the Width/Length/Depth values below.',
        poll=_poll_custom_connector_object,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_width_mm: FloatProperty(
        name='Custom Width (mm)',
        description="Target size along the object's local X axis",
        default=6.0,
        min=0.1,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_length_mm: FloatProperty(
        name='Custom Length (mm)',
        description="Target size along the object's local Y axis",
        default=6.0,
        min=0.1,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_depth_mm: FloatProperty(
        name='Custom Depth (mm)',
        description="Target size along the object's local Z axis (insertion depth)",
        default=8.0,
        min=0.1,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    custom_snap_spheres_enabled: BoolProperty(
        name='Enable Snap Spheres',
        description='Add a ring of snap spheres around the Custom Connector, using Custom Width as the reference axis',
        default=False,
        update=_snapsplit_update_connector_preview,
    )


    # Insert depth
    pin_embed_pct: FloatProperty(
        name='Insert Depth (%)',
        description='Percentage of connector length recessed into part A',
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Dovetail basics
    dovetail_width_mm: FloatProperty(
        name='Dovetail Width (mm)',
        default=6.0,
        min=2.0,
        soft_max=60.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_length_mm: FloatProperty(
        name='Dovetail Length (mm)',
        description='Length along seam plane (local v)',
        default=6.0,
        min=2.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_depth_mm: FloatProperty(
        name='Dovetail Depth (mm)',
        default=8.0,
        min=2.0,
        soft_max=120.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_taper_pct: FloatProperty(
        name='Taper (%)',
        description='Percentage by which the tip is narrower than the base',
        default=25.0,
        min=5.0,
        max=60.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )


    # Tolerances / material profile
    material_profile: EnumProperty(
        name='Material Profiles',
        items=_material_items(),
        default="PLA",
        description='Select a material profile to auto-fill tolerance per side',
    )

    tol_override: FloatProperty(
        name='Tolerance per Face (mm)',
        description='Overrides material profile (0 = use profile value)',
        default=0.0,
        min=0.0,
        soft_max=0.6,
    )

    def effective_tolerance(self) -> float:
        """Return the active tolerance per side, considering the override if set."""
        prof = MATERIAL_PROFILES.get(self.material_profile, 0.2)
        return prof if self.tol_override <= 0.0 else self.tol_override

    # UI foldouts
    ui_more_seg: BoolProperty(
        name='More segmentation settings',
        description='Show advanced segmentation options',
        default=False
    )

    ui_more_conn: BoolProperty(
        name='More connection settings',
        description='Show advanced connection/geometry options',
        default=False
    )

    ui_more_tol: BoolProperty(
        name='More tolerance settings',
        description='Show advanced tolerance options',
        default=False
    )

    # Alignment foldout
    ui_more_align: BoolProperty(
        name='More alignment settings',
        description='Show advanced alignment options',
        default=False
    )

    # ------------------------------------------------------------
    # NEW: Advanced Dovetail controls
    # ------------------------------------------------------------


    # Signed taper override in percent — if non-zero, overrides plain taper in ops.
    dovetail_signed_taper_pct: FloatProperty(
        name='Signed Taper (%)',
        description='Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper.',
        default=0.0,
        soft_min=-60.0,
        soft_max=60.0,
        min=-90.0,
        max=90.0,
        update=_snapsplit_update_connector_preview,
    )

    # Span mode across the seam; UI already supports this.
    dovetail_span_mode: EnumProperty(
        name='Span Mode',
        description='How the dovetail spans along the seam',
        items=[
            ("AUTO", 'Auto', 'Use full edge-to-edge span of the seam'),
            ("FIXED", 'Fixed', 'Use a fixed repeating spacing'),
            ("CENTERED", 'Centered', 'Center block(s) with margins'),
        ],
        default="AUTO",
        update=_snapsplit_update_connector_preview,
    )

    # Margin already present as connector_margin_pct; keep dovetail-specific too if UI expects it.
    dovetail_margin_pct: FloatProperty(
        name='Margin (%)',
        description='Trim percentage at both ends of seam span',
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Force a fixed span axis for the dovetail so it always overshoots the
    # object's outer sides along that axis (for automatic hard-side trimming).
    # NONE keeps the normal margin-based sizing; edges are only trimmed if the
    # separate Hard-side Cut option is enabled manually.
    dovetail_span_axis: EnumProperty(
        name='Span Axis',
        description='Auto stretches along the Dovetail Width axis and trims to the outer sides; X/Y/Z force overshoot along that world axis if it lies in the seam plane; None uses the manually configured Dovetail Length',
        items=[
            ("NONE", 'None', 'Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled'),
            ("AUTO", 'Auto', 'Automatically stretch along the Dovetail Width axis and trim to the outer sides'),
            ("X", "X", 'Force overshoot along world X, if it lies in the seam plane'),
            ("Y", "Y", 'Force overshoot along world Y, if it lies in the seam plane'),
            ("Z", "Z", 'Force overshoot along world Z, if it lies in the seam plane'),
        ],
        default="AUTO",
        update=_snapsplit_update_connector_preview,
    )



    # Prefer a sharp side cut for socket/slot walls.
    # NOTE: intentionally has no live-preview update callback, since the
    # wireframe live preview never performs the boolean hard-side cut
    # (identical behavior to the existing click-placement preview).
    dovetail_hard_side_cut: BoolProperty(
        name='Hard-side Cut',
        description='Prefer sharp side cut for dovetail socket/slot',
        default=False,
    )

    # In-plane placement: offsets (mm) along both seam-plane axes (u = width, v = length)
    # and rotation (deg) within the cut plane.
    dovetail_inplane_offset_u_mm: FloatProperty(
        name='Offset along Width (mm)',
        description='Offset within the cut plane along the width (u) axis to shift the dovetail pattern',
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_inplane_offset_v_mm: FloatProperty(
        name='Offset along Length (mm)',
        description='Offset within the cut plane along the length (v) axis to shift the dovetail pattern',
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_connector_preview,
    )


    dovetail_inplane_rotation_deg: FloatProperty(
        name='Rotation in plane (deg)',
        description='Rotation within the cut plane to orient the dovetail pattern',
        default=0.0,
        soft_min=-180.0,
        soft_max=180.0,
        update=_snapsplit_update_connector_preview,
    )


# ---------------------------
# Registration
# ---------------------------

classes = (SnapSplitProps,)


def register():
    """Register property classes and attach to bpy.types.Scene."""
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.snapsplit = PointerProperty(type=SnapSplitProps)


def unregister():
    """Unregister property classes and detach from bpy.types.Scene."""
    if hasattr(bpy.types.Scene, "snapsplit"):
        del bpy.types.Scene.snapsplit
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
```

---

### seam_data.py

```py
'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''
"""Freehand Cut, stage A: non-destructive stroke and section preview."""

"""Store versioned Freehand seam metadata on result objects."""

# seam_data.py

import json
import math
import bpy
from uuid import uuid4

from mathutils import Vector


SCHEMA_VERSION = 1
OBJECT_ID_KEY = "snapsplit_seam_object_id"
DATA_KEY = "snapsplit_seam_data"


def _coordinates(vector):
    """Convert a vector to JSON-compatible coordinates."""
    return [float(component) for component in vector]


def read_seam_data(obj):
    """Read supported metadata without silently accepting another version."""
    raw = obj.get(DATA_KEY)

    if raw is None:
        return None

    if not isinstance(raw, str):
        raise ValueError(
            f"Invalid seam metadata on '{obj.name}': expected JSON text."
        )

    try:
        data = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Cannot read seam metadata on '{obj.name}'."
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(f"Invalid seam metadata on '{obj.name}'.")

    if data.get("version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported seam metadata version on '{obj.name}'."
        )

    if (
        not isinstance(data.get("object_id"), str)
        or data["object_id"] != obj.get(OBJECT_ID_KEY)
        or not isinstance(data.get("seams"), list)
    ):
        raise ValueError(
            f"Inconsistent seam metadata on '{obj.name}'."
        )

    return data


def write_freehand_seams(
    objects,
    regions,
    plane_point,
    plane_normal,
    tangent,
    capped,
    tolerance,
):
    """Write reciprocal seam records on newly created result objects only."""
    if len(objects) < 2 or not regions:
        raise ValueError("No valid Freehand seam relationships were prepared.")

    normal_world = Vector(plane_normal).normalized()
    tangent_world = Vector(tangent).normalized()

    object_ids = [uuid4().hex for _obj in objects]
    documents = [
        {
            "version": SCHEMA_VERSION,
            "object_id": object_id,
            "seams": [],
        }
        for object_id in object_ids
    ]

    for region in regions:
        negative = region["negative_part"]
        positive = region["positive_part"]

        if (
            not 0 <= negative < len(objects)
            or not 0 <= positive < len(objects)
            or negative == positive
        ):
            raise ValueError("A seam has invalid result partners.")

        seam_id = uuid4().hex

        for own_index, partner_index, side in (
            (negative, positive, -1),
            (positive, negative, 1),
        ):
            obj = objects[own_index]
            matrix = obj.matrix_world
            inverse = matrix.inverted()

            # A world-space plane normal becomes local via M transposed.
            normal_local = (
                matrix.to_3x3().transposed() @ normal_world
            ).normalized()

            # A tangent is a direction, not a normal.
            tangent_local = (
                inverse.to_3x3() @ tangent_world
            ).normalized()

            def local_loop(points):
                return [
                    _coordinates(inverse @ Vector(point))
                    for point in points
                ]

            record = {
                "seam_id": seam_id,
                "kind": "FREEHAND",
                "partner_id": object_ids[partner_index],
                "side": side,
                "capped_at_creation": bool(capped),
                "plane_point_local": _coordinates(
                    inverse @ Vector(plane_point)
                ),
                "plane_normal_local": _coordinates(normal_local),
                "tangent_local": _coordinates(tangent_local),
                "outer_local": local_loop(region["outer"]),
                "holes_local": [
                    local_loop(hole)
                    for hole in region["holes"]
                ],
                "tolerance_world_at_creation": float(tolerance),
            }

            documents[own_index]["seams"].append(record)

    if any(not document["seams"] for document in documents):
        raise ValueError("A result object has no assigned Freehand seam.")

    # Serialize everything before modifying any object properties.
    serialized = [
        json.dumps(
            document,
            separators=(",", ":"),
            allow_nan=False,
        )
        for document in documents
    ]

    for obj, object_id, raw in zip(objects, object_ids, serialized):
        obj[OBJECT_ID_KEY] = object_id
        obj[DATA_KEY] = raw


def describe_seams(obj):
    """Return concise diagnostic lines without changing scene data."""
    data = read_seam_data(obj)

    if data is None:
        return [f"{obj.name}: no Freehand seam metadata"]

    lines = [
        f"{obj.name}: object_id={data['object_id']}, "
        f"seams={len(data['seams'])}"
    ]

    for record in data["seams"]:
        state = (
            "capped at creation"
            if record["capped_at_creation"]
            else "open at creation"
        )
        lines.append(
            f"  seam={record['seam_id']} "
            f"partner={record['partner_id']} "
            f"side={record['side']:+d} "
            f"holes={len(record['holes_local'])} "
            f"state={state}"
        )

    return lines

class SeamValidationError(ValueError):
    """Indicate invalid, unsupported, or ambiguous Freehand seam data."""


def has_freehand_metadata(obj):
    """Reserve active and archived Freehand objects for explicit resolution."""
    return (
        obj is not None
        and (
            DATA_KEY in obj
            or OBJECT_ID_KEY in obj
            or "snapsplit_seam_archive" in obj
        )
    )



def _checked_vector(value, label):
    """Read a finite three-dimensional vector from JSON data."""
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 3
        or any(
            isinstance(component, bool)
            or not isinstance(component, (int, float))
            or not math.isfinite(component)
            for component in value
        )
    ):
        raise SeamValidationError(f"Invalid {label}.")

    return Vector(value)


def _checked_loop(value, label):
    """Read a polygon boundary without accepting degenerate loops."""
    if not isinstance(value, list) or len(value) < 3:
        raise SeamValidationError(f"Invalid {label}.")

    return [
        _checked_vector(point, label)
        for point in value
    ]


def _validated_document(obj):
    """Validate object identity and the complete local seam record list."""
    try:
        document = read_seam_data(obj)
    except ValueError as exc:
        raise SeamValidationError(str(exc)) from exc

    if document is None:
        raise SeamValidationError(
            f"Missing Freehand seam data on '{obj.name}'."
        )

    object_id = document["object_id"]
    if not object_id:
        raise SeamValidationError("An object ID is empty.")

    holders = [
        candidate
        for candidate in bpy.data.objects
        if candidate.get(OBJECT_ID_KEY) == object_id
    ]

    if len(holders) != 1 or holders[0] != obj:
        raise SeamValidationError(
            f"Duplicate or ambiguous seam object ID on '{obj.name}'."
        )

    records = document["seams"]
    if not records:
        raise SeamValidationError("The seam record list is empty.")

    seen = set()

    for record in records:
        if not isinstance(record, dict):
            raise SeamValidationError("A seam record is not a dictionary.")

        seam_id = record.get("seam_id")
        partner_id = record.get("partner_id")

        if (
            not isinstance(seam_id, str)
            or not seam_id
            or seam_id in seen
            or not isinstance(partner_id, str)
            or not partner_id
            or partner_id == object_id
            or record.get("kind") != "FREEHAND"
        ):
            raise SeamValidationError("Invalid seam identity or partner.")

        seen.add(seam_id)

        if (
            type(record.get("side")) is not int
            or record["side"] not in (-1, 1)
            or type(record.get("capped_at_creation")) is not bool
        ):
            raise SeamValidationError("Invalid seam side or cap status.")

        for key in (
            "plane_point_local",
            "plane_normal_local",
            "tangent_local",
        ):
            _checked_vector(record.get(key), key)

        _checked_loop(record.get("outer_local"), "outer contour")

        holes = record.get("holes_local")
        if not isinstance(holes, list):
            raise SeamValidationError("Invalid inner contour list.")

        for hole in holes:
            _checked_loop(hole, "inner contour")

        tolerance = record.get("tolerance_world_at_creation")
        if (
            isinstance(tolerance, bool)
            or not isinstance(tolerance, (int, float))
            or not math.isfinite(tolerance)
            or tolerance <= 0.0
        ):
            raise SeamValidationError("Invalid stored seam tolerance.")

    return document


def _world_record(obj, record):
    """Transform a seam frame and its boundaries into current world space."""
    if obj.type != 'MESH' or obj.data is None:
        raise SeamValidationError("Freehand partners must be mesh objects.")

    if obj.mode != 'OBJECT':
        raise SeamValidationError("Switch both partners to Object Mode.")

    if any(
        modifier.show_viewport or modifier.show_render
        for modifier in obj.modifiers
    ):
        raise SeamValidationError(
            f"Active modifiers are not supported on '{obj.name}' in C2."
        )

    matrix = obj.matrix_world
    linear = matrix.to_3x3()
    determinant = linear.determinant()

    if not math.isfinite(determinant) or determinant <= 1e-12:
        raise SeamValidationError(
            "Singular, mirrored, or extremely small transforms are unsupported."
        )

    if any(
        not math.isfinite(matrix[row][column])
        for row in range(4)
        for column in range(4)
    ):
        raise SeamValidationError("The object transform contains invalid values.")

    local_normal = _checked_vector(
        record["plane_normal_local"], "local normal"
    )
    local_tangent = _checked_vector(
        record["tangent_local"], "local tangent"
    )

    normal = linear.inverted().transposed() @ local_normal
    tangent = linear @ local_tangent

    if normal.length <= 1e-12:
        raise SeamValidationError("The seam normal is degenerate.")

    normal.normalize()
    tangent -= normal * tangent.dot(normal)

    if tangent.length <= 1e-12:
        raise SeamValidationError("The seam tangent is degenerate.")

    tangent.normalize()

    loops = [
        [
            matrix @ point
            for point in _checked_loop(
                record["outer_local"], "outer contour"
            )
        ]
    ]

    loops.extend(
        [
            matrix @ point
            for point in _checked_loop(hole, "inner contour")
        ]
        for hole in record["holes_local"]
    )

    return {
        "origin": matrix @ _checked_vector(
            record["plane_point_local"], "plane point"
        ),
        "normal": normal,
        "tangent": tangent,
        "loops": loops,
        "side": record["side"],
    }


def _loops_match(first, second, tolerance):
    """Compare polygon cycles independent of start vertex and traversal."""
    if len(first) != len(second):
        return False

    count = len(first)

    for start in range(count):
        for direction in (-1, 1):
            if all(
                (
                    first[index]
                    - second[(start + direction * index) % count]
                ).length <= tolerance
                for index in range(count)
            ):
                return True

    return False


def _boundaries_match(first, second, tolerance):
    """Compare an outer contour and an unordered list of inner contours."""
    if (
        len(first) != len(second)
        or not _loops_match(first[0], second[0], tolerance)
    ):
        return False

    remaining = list(second[1:])

    for hole in first[1:]:
        match = next(
            (
                index
                for index, candidate in enumerate(remaining)
                if _loops_match(hole, candidate, tolerance)
            ),
            None,
        )

        if match is None:
            return False

        remaining.pop(match)

    return not remaining


def _loop_area(loop, origin, x_axis, y_axis):
    """Measure an unsigned polygon area in the seam plane."""
    points = [
        (
            (point - origin).dot(x_axis),
            (point - origin).dot(y_axis),
        )
        for point in loop
    ]

    return abs(
        0.5 * sum(
            points[index][0] * points[(index + 1) % len(points)][1]
            - points[(index + 1) % len(points)][0] * points[index][1]
            for index in range(len(points))
        )
    )


def _verify_current_cap(obj, frame, tolerance):
    """Verify a current planar cap island against its stored boundary edges."""
    mesh = obj.data
    matrix = obj.matrix_world
    vertices = [
        matrix @ vertex.co
        for vertex in mesh.vertices
    ]

    if any(
        not math.isfinite(component)
        for point in vertices
        for component in point
    ):
        raise SeamValidationError("The current mesh contains invalid vertices.")

    origin = frame["origin"]
    normal = frame["normal"]
    edge_faces = {}

    for face in mesh.polygons:
        for edge in face.edge_keys:
            key = tuple(sorted(edge))
            edge_faces.setdefault(key, []).append(face.index)

    # Require a closed edge-manifold surface, including any cavity walls.
    if (
        any(
            len(edge_faces.get(tuple(sorted(edge.vertices)), ())) != 2
            for edge in mesh.edges
        )
        or any(len(faces) != 2 for faces in edge_faces.values())
    ):
        raise SeamValidationError(
            f"'{obj.name}' is open or contains non-manifold edges."
        )

    planar = {
        face.index
        for face in mesh.polygons
        if all(
            abs((vertices[index] - origin).dot(normal)) <= tolerance
            for index in face.vertices
        )
    }

    expected_edges = [
        (loop[index], loop[(index + 1) % len(loop)])
        for loop in frame["loops"]
        for index in range(len(loop))
    ]

    def matches_edge(key, expected):
        a, b = (vertices[index] for index in key)
        c, d = expected
        return (
            (a - c).length <= tolerance
            and (b - d).length <= tolerance
        ) or (
            (a - d).length <= tolerance
            and (b - c).length <= tolerance
        )

    seed_faces = {
        face_index
        for key, linked in edge_faces.items()
        if matches_edge(key, expected_edges[0])
        for face_index in linked
        if face_index in planar
    }

    if len(seed_faces) != 1:
        raise SeamValidationError(
            "The stored contour does not identify a unique current cap."
        )

    adjacency = {index: set() for index in planar}

    for linked in edge_faces.values():
        if linked[0] in planar and linked[1] in planar:
            adjacency[linked[0]].add(linked[1])
            adjacency[linked[1]].add(linked[0])

    island = set()
    pending = list(seed_faces)

    while pending:
        index = pending.pop()
        if index in island:
            continue
        island.add(index)
        pending.extend(adjacency[index] - island)

    boundary = [
        key
        for key, linked in edge_faces.items()
        if sum(index in island for index in linked) == 1
    ]

    if len(boundary) != len(expected_edges):
        raise SeamValidationError(
            "The current cap boundary differs from the stored contours."
        )

    remaining = list(boundary)

    for expected in expected_edges:
        matches = [
            index
            for index, key in enumerate(remaining)
            if matches_edge(key, expected)
        ]

        if len(matches) != 1:
            raise SeamValidationError(
                "A stored contour edge is missing or ambiguous."
            )

        remaining.pop(matches[0])

    # Positive-side parts have outward cap normals pointing to the negative side.
    expected_normal = normal * -frame["side"]
    area = 0.0

    for index in island:
        face = mesh.polygons[index]
        points = [vertices[item] for item in face.vertices]
        reference = points[0]
        area_vector = Vector((0.0, 0.0, 0.0))

        for item in range(1, len(points) - 1):
            area_vector += (
                (points[item] - reference).cross(
                    points[item + 1] - reference
                ) * 0.5
            )

        if (
            area_vector.length <= tolerance * tolerance
            or area_vector.normalized().dot(expected_normal) < 1.0 - 1e-5
        ):
            raise SeamValidationError(
                "A cap face is degenerate or has an inconsistent orientation."
            )

        area += area_vector.length

    x_axis = frame["tangent"]
    y_axis = normal.cross(x_axis).normalized()
    expected_area = (
        _loop_area(frame["loops"][0], origin, x_axis, y_axis)
        - sum(
            _loop_area(hole, origin, x_axis, y_axis)
            for hole in frame["loops"][1:]
        )
    )

    if (
        expected_area <= tolerance * tolerance
        or abs(area - expected_area)
        > max(expected_area * 1e-5, tolerance * tolerance * 32.0)
    ):
        raise SeamValidationError(
            "The current cap area differs from the stored material region."
        )


def resolve_freehand_plane(obj_p, obj_q):
    """Resolve a validated Freehand seam without enabling connector placement.

    Return (socket, pin, origin, normal, tangent), or None when neither object
    has Freehand metadata or when two valid documents have no shared seam.
    Raise SeamValidationError for invalid or unsupported relationships.
    """
    if not (
        has_freehand_metadata(obj_p)
        or has_freehand_metadata(obj_q)
    ):
        return None

    if obj_p == obj_q:
        raise SeamValidationError("Select two different seam partners.")

    if not (
        has_freehand_metadata(obj_p)
        and has_freehand_metadata(obj_q)
    ):
        raise SeamValidationError(
            "Only one selected object has Freehand seam metadata."
        )

    p_data = _validated_document(obj_p)
    q_data = _validated_document(obj_q)

    p_records = [
        record
        for record in p_data["seams"]
        if record["partner_id"] == q_data["object_id"]
    ]
    q_records = [
        record
        for record in q_data["seams"]
        if record["partner_id"] == p_data["object_id"]
    ]

    if not p_records and not q_records:
        return None

    if (
        len(p_records) != 1
        or len(q_records) != 1
        or p_records[0]["seam_id"] != q_records[0]["seam_id"]
    ):
        raise SeamValidationError(
            "The partner relationship is missing, asymmetric, or ambiguous."
        )

    p_record, q_record = p_records[0], q_records[0]

    if p_record["side"] != -q_record["side"]:
        raise SeamValidationError("The seam sides are not opposite.")

    if not (
        p_record["capped_at_creation"]
        and q_record["capped_at_creation"]
    ):
        raise SeamValidationError(
            "Open Freehand seams are not supported for connectors in C2."
        )

    p_frame = _world_record(obj_p, p_record)
    q_frame = _world_record(obj_q, q_record)

    span = max(
        (point - p_frame["loops"][0][0]).length
        for loop in p_frame["loops"]
        for point in loop
    )

    # Derive tolerance from current world dimensions, not stale creation scale.
    tolerance = max(1e-7, span * 1e-6)

    if (
        p_frame["normal"].dot(q_frame["normal"]) < 1.0 - 1e-6
        or p_frame["tangent"].dot(q_frame["tangent"]) < 1.0 - 1e-6
        or (p_frame["origin"] - q_frame["origin"]).length > tolerance
        or not _boundaries_match(
            p_frame["loops"], q_frame["loops"], tolerance
        )
    ):
        raise SeamValidationError(
            "The two seam frames or contours no longer coincide."
        )

    for frame in (p_frame, q_frame):
        if any(
            abs((point - frame["origin"]).dot(frame["normal"])) > tolerance
            for loop in frame["loops"]
            for point in loop
        ):
            raise SeamValidationError("A stored contour is not planar.")

    _verify_current_cap(obj_p, p_frame, tolerance)
    _verify_current_cap(obj_q, q_frame, tolerance)

    if p_frame["side"] == 1:
        socket, pin = obj_p, obj_q
    else:
        socket, pin = obj_q, obj_p

    return (
        socket,
        pin,
        p_frame["origin"],
        p_frame["normal"],
        p_frame["tangent"],
    )

```

---

### seam_migration.py

```py
# -*- coding: utf-8 -*-
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# seam_migration.py
"""Migrate intact Freehand seams when a result object is cut again."""

import copy
import json

import bpy

from .seam_data import (
    DATA_KEY,
    OBJECT_ID_KEY,
    SeamValidationError,
    _validated_document,
    _verify_current_cap,
    _world_record,
    read_seam_data,
)


ARCHIVE_KEY = "snapsplit_seam_archive"


def _encode(document):
    """Serialize metadata before committing any property changes."""
    return json.dumps(
        document,
        separators=(",", ":"),
        allow_nan=False,
    )


def _snapshot(obj):
    """Capture only properties owned by this migration."""
    return (
        obj,
        {
            key: obj[key] if key in obj else None
            for key in (DATA_KEY, OBJECT_ID_KEY, ARCHIVE_KEY)
        },
    )


def _restore(snapshot):
    """Restore a previously captured metadata state."""
    obj, values = snapshot

    for key, value in values.items():
        if value is None:
            if key in obj:
                del obj[key]
        else:
            obj[key] = value


def _find_partner(object_id):
    """Resolve an active object ID without depending on object names."""
    matches = [
        obj
        for obj in bpy.data.objects
        if obj.get(OBJECT_ID_KEY) == object_id
    ]

    if len(matches) != 1:
        raise SeamValidationError(
            "An existing seam partner is missing or has a duplicate object ID."
        )

    return matches[0]


def _counterpart(document, source_id, seam_id):
    """Find exactly one reciprocal record in a partner document."""
    matches = [
        record
        for record in document["seams"]
        if record["partner_id"] == source_id
        and record["seam_id"] == seam_id
    ]

    if len(matches) != 1:
        raise SeamValidationError(
            "An existing seam has a missing or ambiguous reciprocal record."
        )

    return matches[0]


def _frame_tolerance(frame):
    """Use the same current-world scale convention as the C2 resolver."""
    reference = frame["loops"][0][0]
    span = max(
        (point - reference).length
        for loop in frame["loops"]
        for point in loop
    )
    return max(1e-7, span * 1e-6)


def _record_for_object(record, frame, obj):
    """Rebase an existing world-space seam onto its new owner."""
    result = copy.deepcopy(record)
    matrix = obj.matrix_world
    inverse = matrix.inverted()

    normal_local = (
        matrix.to_3x3().transposed() @ frame["normal"]
    ).normalized()

    tangent_local = (
        inverse.to_3x3() @ frame["tangent"]
    ).normalized()

    def coordinates(vector):
        return [float(component) for component in vector]

    def local_loop(loop):
        return [
            coordinates(inverse @ point)
            for point in loop
        ]

    result["plane_point_local"] = coordinates(
        inverse @ frame["origin"]
    )
    result["plane_normal_local"] = coordinates(normal_local)
    result["tangent_local"] = coordinates(tangent_local)
    result["outer_local"] = local_loop(frame["loops"][0])
    result["holes_local"] = [
        local_loop(loop)
        for loop in frame["loops"][1:]
    ]

    return result


def migrate_intact_freehand_seams(source, results):
    """Transfer intact contacts without blocking cuts on modified old caps.

    Modified, divided, or ambiguous old relationships are removed from
    active seam documents and preserved in contact history.

    Existing connector mesh geometry is never modified here.
    Return a callback restoring all metadata changed by this function.
    """
    history_key = "snapsplit_contact_history"
    property_keys = (
        DATA_KEY,
        OBJECT_ID_KEY,
        ARCHIVE_KEY,
        history_key,
    )

    if ARCHIVE_KEY in source:
        raise SeamValidationError(
            "This object is an archived cut source."
        )

    if DATA_KEY not in source and OBJECT_ID_KEY not in source:
        return lambda: None

    results = list(results)
    source_pointer = source.as_pointer()
    result_pointers = [obj.as_pointer() for obj in results]

    if (
        len(results) < 2
        or len(set(result_pointers)) != len(results)
        or source_pointer in result_pointers
    ):
        raise SeamValidationError(
            "Migration requires at least two distinct new result objects."
        )

    source_document = copy.deepcopy(_validated_document(source))
    source_id = source_document["object_id"]

    result_documents = []
    for obj in results:
        if ARCHIVE_KEY in obj:
            raise SeamValidationError(
                "A new result unexpectedly contains archived metadata."
            )
        result_documents.append(
            copy.deepcopy(_validated_document(obj))
        )

    partners = {}
    events = []
    event_targets = []

    def matrix_values(obj):
        """Store the current placement independently of object names."""
        return [
            [
                float(obj.matrix_world[row][column])
                for column in range(4)
            ]
            for row in range(4)
        ]

    def read_history(obj):
        """Preserve previous history instead of silently overwriting it."""
        if history_key not in obj:
            return []

        raw = obj[history_key]
        if not isinstance(raw, str):
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is not JSON text."
            )

        try:
            value = json.loads(raw)
        except (TypeError, ValueError) as exc:
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is invalid."
            ) from exc

        if not isinstance(value, list):
            raise SeamValidationError(
                f"Contact history on '{obj.name}' is not a list."
            )

        return value

    for old_record in source_document["seams"]:
        seam_id = old_record["seam_id"]
        partner_id = old_record["partner_id"]

        if partner_id not in partners:
            partner = _find_partner(partner_id)
            pointer = partner.as_pointer()

            if (
                pointer == source_pointer
                or pointer in result_pointers
                or ARCHIVE_KEY in partner
            ):
                raise SeamValidationError(
                    "An existing contact has an invalid external partner."
                )

            partners[partner_id] = (
                partner,
                copy.deepcopy(_validated_document(partner)),
            )

        partner, partner_document = partners[partner_id]
        reciprocal = _counterpart(
            partner_document,
            source_id,
            seam_id,
        )

        if reciprocal["side"] != -old_record["side"]:
            raise SeamValidationError(
                "An existing contact has inconsistent reciprocal sides."
            )

        # Preserve both original records before editing their relationship.
        event = {
            "previous_seam_id": seam_id,
            "source_id": source_id,
            "partner_id": partner_id,
            "source_record": copy.deepcopy(old_record),
            "partner_record": copy.deepcopy(reciprocal),
            "source_matrix_world": matrix_values(source),
            "partner_matrix_world": matrix_values(partner),
        }

        owners = []

        if old_record["capped_at_creation"]:
            # Local metadata follows the source's current placement.
            # The external partner need not currently coincide with it.
            frame = _world_record(source, old_record)
            tolerance = _frame_tolerance(frame)

            for index, obj in enumerate(results):
                try:
                    _verify_current_cap(obj, frame, tolerance)
                except SeamValidationError:
                    # A changed old cap must not block a new mesh cut.
                    continue
                owners.append(index)

        if len(owners) == 1:
            owner_index = owners[0]
            owner = results[owner_index]
            owner_document = result_documents[owner_index]

            if any(
                record["seam_id"] == seam_id
                for record in owner_document["seams"]
            ):
                raise SeamValidationError(
                    "A migrated seam ID already exists on its new owner."
                )

            migrated = _record_for_object(
                old_record,
                frame,
                owner,
            )
            migrated["side"] = old_record["side"]
            migrated["partner_id"] = partner_id
            owner_document["seams"].append(migrated)

            # Keep the partner's own local geometry and placement unchanged.
            reciprocal["partner_id"] = owner_document["object_id"]

            event["action"] = "TRANSFERRED"
            event["new_owner_id"] = owner_document["object_id"]
            targets = [source, partner, owner]

        else:
            # Do not retain an active link to an archived source.
            # The complete old relationship survives in the history.
            partner_document["seams"].remove(reciprocal)

            event["action"] = "RETIRED"
            event["reason"] = (
                "The old contact was open, modified, divided, or "
                "could not be assigned to one intact result cap."
            )
            targets = [source, partner, *results]

        events.append(event)
        event_targets.append(targets)

    touched = {}
    for obj in [
        source,
        *results,
        *(obj for obj, _document in partners.values()),
    ]:
        touched[obj.as_pointer()] = obj

    histories = {
        pointer: read_history(obj)
        for pointer, obj in touched.items()
    }

    for event, targets in zip(events, event_targets):
        seen = set()
        for obj in targets:
            pointer = obj.as_pointer()
            if pointer not in seen:
                histories[pointer].append(copy.deepcopy(event))
                seen.add(pointer)

    # Prepare all payloads before changing any existing properties.
    writes = []

    for obj, document in zip(results, result_documents):
        writes.append((obj, DATA_KEY, _encode(document)))

    for partner, document in partners.values():
        if document["seams"]:
            writes.append((partner, DATA_KEY, _encode(document)))
        else:
            # An empty active document would fail the existing validator.
            # History alone must not mark the partner as archived.
            writes.append((partner, DATA_KEY, None))
            writes.append((partner, OBJECT_ID_KEY, None))

    for pointer, obj in touched.items():
        writes.append((
            obj,
            history_key,
            _encode(histories[pointer]),
        ))

    archive = {
        "version": 1,
        "state": "REPLACED_BY_FREEHAND_RESULTS",
        "previous_document": source_document,
        "transfers": events,
    }

    writes.extend([
        (source, ARCHIVE_KEY, _encode(archive)),
        (source, DATA_KEY, None),
        (source, OBJECT_ID_KEY, None),
    ])

    snapshots = [
        (
            obj,
            {
                key: (
                    key in obj,
                    copy.deepcopy(obj[key]) if key in obj else None,
                )
                for key in property_keys
            },
        )
        for obj in touched.values()
    ]

    def rollback():
        """Restore every touched property, attempting all restorations."""
        failures = []

        for obj, values in reversed(snapshots):
            for key, (existed, value) in values.items():
                try:
                    if existed:
                        obj[key] = copy.deepcopy(value)
                    elif key in obj:
                        del obj[key]
                except Exception as exc:
                    failures.append(f"{key}: {exc}")

        if failures:
            raise RuntimeError(
                "Contact metadata rollback failed: "
                + "; ".join(failures)
            )

    try:
        for obj, key, value in writes:
            if value is None:
                if key in obj:
                    del obj[key]
            else:
                obj[key] = value

        for obj in results:
            _validated_document(obj)

        for partner, document in partners.values():
            if document["seams"]:
                _validated_document(partner)

    except Exception as exc:
        try:
            rollback()
        except Exception as rollback_exc:
            raise RuntimeError(
                f"Contact migration failed: {exc}. "
                f"Rollback also failed: {rollback_exc}"
            ) from exc
        raise

    return rollback



```

---

### ui.py

```py
# -*- coding: utf-8 -*-
"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

# ui.py

import bpy
from bpy.types import Panel
from .utils import is_lang_de  # kept import (may be used elsewhere)
from .profiles import MATERIAL_PROFILES  # used for tolerance preview


def _exists(obj, attr):
    """Small helper to guard missing properties in early integration phases."""
    try:
        getattr(obj, attr)
        return True
    except Exception:
        return False


class SNAP_PT_panel(Panel):
    """Main SnapSplit UI panel in the 3D Viewport N-Panel."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        # Keep enabled as long as a scene exists.
        return context is not None and context.scene is not None

    def draw(self, context):
        # Draw localized UI using tr(); do not alter underlying behavior.
        layout = self.layout
        props = getattr(context.scene, "snapsplit", None)

        if props is None:
            layout.label(text='SnapSplit properties not available.', icon="ERROR")
            layout.label(text='Please re-enable the Add-on.')
            return

        # =========================
        # SEGMENTATION
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text='Segmentation', icon='MOD_BOOLEAN')
        more_txt = 'Less...' if getattr(props, "ui_more_seg", False) else 'More...'
        if _exists(props, "ui_more_seg"):
            header.prop(props, "ui_more_seg", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "split_axis"):
            col.prop(props, "split_axis", text='Split Axis')

        row = col.row(align=True)
        if _exists(props, "show_split_preview"):
            row.prop(props, "show_split_preview", text='Show split preview')
        row.operator("snapsplit.adjust_split_axis",
                     icon="EMPTY_AXIS",
                     text='Adjust')

        if getattr(props, "ui_more_seg", False):
            adv = box.column(align=True)
            if _exists(props, "parts_count"):
                adv.prop(props, "parts_count", text='Number of Parts')
                try:
                    if int(getattr(props, "parts_count")) >= 12:
                        adv.label(icon='INFO', text='High part count may be slow')
                except Exception:
                    pass
            if _exists(props, "split_offset_mm"):
                adv.prop(props, "split_offset_mm", text='Split Offset (mm)')
            if _exists(props, "cap_seams_during_split"):
                adv.prop(props, "cap_seams_during_split",
                         text='Cap seams during split')
                if not getattr(props, "cap_seams_during_split", False):
                    sub = adv.column(align=True)
                    sub.operator("snapsplit.cap_open_seams_now",
                                 icon="OUTLINER_OB_SURFACE",
                                 text='Cap seams now')
                    sub.label(text="To close existing seams, run 'Cap seams now'.", icon='INFO')

        col_bottom = box.column(align=True)
        col_bottom.operator("snapsplit.planar_split",
                            icon="MOD_BOOLEAN",
                            text='Planar Split')

        # Invoke the modal preview in the viewport WINDOW region.
        freehand_row = col_bottom.row(align=True)
        freehand_row.operator_context = 'INVOKE_REGION_WIN'

        freehand_row.operator(
            "snapsplit.freehand_cut",
            icon='GREASEPENCIL',
            text='Freehand Cut',
        )

        layout.separator()


        # =========================
        # CONNECTIONS
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text='Connections', icon='SNAP_FACE')
        more_txt = 'Less...' if getattr(props, "ui_more_conn", False) else 'More...'
        if _exists(props, "ui_more_conn"):
            header.prop(props, "ui_more_conn", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "connector_type"):
            col.prop(props, "connector_type", text='Connector Type')
        if _exists(props, "connector_distribution"):
            col.prop(props, "connector_distribution", text='Distribution')

        # Live wireframe preview toggle for LINE/GRID connector placement.
        # Independent of connector_type, since the preview builder itself
        # decides per-type what shape/ring to draw. Capped at 200 objects
        # internally (see ops_connectors.update_connector_placement_preview).
        if _exists(props, "connector_live_preview"):
            col.prop(props, "connector_live_preview", text='Live Preview')

        # Pin/socket role switch (applies to Add Connectors, live preview and click placement)
        if _exists(props, "swap_pin_socket"):
            col.prop(props, "swap_pin_socket", text='Swap Pin / Socket')


        # Action buttons
        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors", icon="SNAP_FACE", text='Add connectors')
        col.operator("snapsplit.place_connectors_click", icon="CURSOR", text='Place connectors (click)')

        if getattr(props, "ui_more_conn", False):
            adv = box.column(align=True)
            dist = getattr(props, "connector_distribution", "LINE")
            if dist == "LINE":
                if _exists(props, "connectors_per_seam"):
                    adv.prop(props, "connectors_per_seam", text='Connectors per Seam')
            else:
                r = adv.row(align=True)
                if _exists(props, "connectors_per_seam"):
                    r.prop(props, "connectors_per_seam", text='Columns')
                if _exists(props, "connectors_rows"):
                    r.prop(props, "connectors_rows", text='Rows')

            if _exists(props, "connector_margin_pct"):
                adv.prop(props, "connector_margin_pct", text='Margin (%)')



            # Connector-specific geometry/settings
            gbox = box.box()
            ctype = getattr(props, "connector_type", "CYL_PIN")


            # --- Pin-like connectors ---
            if ctype in {"CYL_PIN", "SNAP_PIN"}:
                if _exists(props, "pin_diameter_mm"):
                    gbox.prop(props, "pin_diameter_mm", text='Pin Diameter (mm)')
                if _exists(props, "pin_length_mm"):
                    gbox.prop(props, "pin_length_mm", text='Pin Length (mm)')
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text='Insert Depth (%)')

                rr = gbox.row(align=True)
                if _exists(props, "pin_segments"):
                    rr.prop(props, "pin_segments", text='Segments')
                try:
                    from .profiles import _suggest_pin_segments_from_diameter
                    diameter = float(getattr(props, "pin_diameter_mm", 5.0))
                    suggested = _suggest_pin_segments_from_diameter(diameter)
                    hint = 'Suggested: ' + f"{suggested}"
                    sub = rr.row(align=True)
                    sub.alignment = 'RIGHT'
                    sub.label(text=hint, icon='INFO')
                except Exception:
                    pass

                # Both remaining pin types (CYL_PIN, SNAP_PIN) support a chamfer
                if _exists(props, "add_chamfer_mm"):
                    gbox.prop(props, "add_chamfer_mm", text='Chamfer (mm)')



                if ctype == "SNAP_PIN" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.column(align=True)
                    s.label(text='Snap spheres:', icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text='Spheres per side')
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text='Sphere Diameter (mm)')
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text='Protrusion (mm)')


            # --- Tenon-like connectors ---
            elif ctype in {"RECT_TENON", "SNAP_TENON"}:
                if _exists(props, "tenon_width_mm"):
                    gbox.prop(props, "tenon_width_mm", text='Tenon Width (mm)')
                if _exists(props, "tenon_depth_mm"):
                    gbox.prop(props, "tenon_depth_mm", text='Tenon Depth (mm)')
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text='Insert Depth (%)')

                # Both remaining tenon types (RECT_TENON, SNAP_TENON) support a chamfer
                if _exists(props, "add_chamfer_mm"):
                    gbox.prop(props, "add_chamfer_mm", text='Chamfer (mm)')



                if ctype == "SNAP_TENON" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.column(align=True)
                    s.label(text='Snap spheres:', icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text='Spheres per side')
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text='Sphere Diameter (mm)')
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text='Protrusion (mm)')

            # --- Dovetail connector ---
            # NOTE: extended from "ctype == \"DOVETAIL\"" to also cover the new
            # Snap Dovetail connector, which shares the exact same wedge geometry
            # (Base size, Signed Taper, Span Axis, Hard-side Cut, Placement).
            elif ctype in {"DOVETAIL", "SNAP_DOVETAIL"}:
                # Base size group  ordered: Width  Length  Depth
                base_box = gbox.box()
                base_box.label(text='Base size', icon='MESH_CUBE')
                if _exists(props, "dovetail_width_mm"):
                    base_box.prop(props, "dovetail_width_mm", text='Dovetail Width (mm)')
                # CRITICAL: Explicit Dovetail Length in UI
                if _exists(props, "dovetail_length_mm"):
                    base_box.prop(props, "dovetail_length_mm", text='Dovetail Length (mm)')
                if _exists(props, "dovetail_depth_mm"):
                    base_box.prop(props, "dovetail_depth_mm", text='Dovetail Depth (mm)')
                if _exists(props, "add_chamfer_mm"):
                    base_box.prop(props, "add_chamfer_mm", text='Chamfer (mm)')

                # Taper (signed) comes next

                if _exists(props, "dovetail_signed_taper_pct"):
                    base_box.prop(props, "dovetail_signed_taper_pct", text='Signed Taper (%)')

                if _exists(props, "dovetail_span_axis"):
                    base_box.prop(props, "dovetail_span_axis", text='Span Axis')
                    if str(getattr(props, "dovetail_span_axis", "NONE")) != "NONE":
                        base_box.label(text='Forces hard-side cut along this axis.', icon='INFO')


                 # Hard-side Cut
                if _exists(props, "dovetail_hard_side_cut"):
                    base_box.prop(props, "dovetail_hard_side_cut", text='Hard-side Cut')

                # NEW: Snap Options box, only shown for the Snap Dovetail variant.
                # Same label/prop pattern as SNAP_PIN / SNAP_TENON so the panel
                # stays visually consistent across all snap-capable connectors.
                if ctype == "SNAP_DOVETAIL" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.box()
                    s.label(text='Snap spheres:', icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text='Spheres per side')
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text='Sphere Diameter (mm)')
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text='Protrusion (mm)')

                # Span options after taper
                # span_box = gbox.box()
                # span_box.label(text=tr("ui.dovetail_span", "Span along seam"), icon='ORIENTATION_GLOBAL')
                # if _exists(props, "dovetail_span_mode"):
                #     span_box.prop(props, "dovetail_span_mode", text=tr("ui.dovetail_span_mode", "Span Mode"))
                # if _exists(props, "dovetail_margin_pct"):
                #     span_box.prop(props, "dovetail_margin_pct", text=tr("ui.dovetail_margin_pct", "Margin (%)"))
                # if _exists(props, "dovetail_auto_span"):
                #     span_box.prop(props, "dovetail_auto_span", text=tr("ui.dovetail_auto_span", "Auto span along seam"))
                # if _exists(props, "dovetail_span_margin_pct"):
                #     span_box.prop(props, "dovetail_span_margin_pct", text=tr("ui.dovetail_span_margin_pct", "Auto-span End Margin (%)"))
                # span_box.label(text=tr("ui.auto_span_hint", "AUTO span = edge-to-edge along seam; # margin trims ends."), icon='INFO')

                # Placement
                extra = gbox.box()
                # extra.label(text=tr("ui.dovetail_extra", "Placement & Sides"),  icon='ORIENTATION_GIMBAL')
                # In-plane placement controls (offsets along width/length + rotation)
                # Ensures "Rotation in plane" is visible; ops already apply it in placement and preview.
                extra.label(text='Placement', icon='ORIENTATION_GLOBAL')
                if _exists(props, "dovetail_inplane_offset_u_mm") or _exists(props, "dovetail_inplane_offset_v_mm") or _exists(props, "dovetail_inplane_rotation_deg"):
                    s = gbox.box()
                    if _exists(props, "dovetail_inplane_offset_u_mm"):
                        s.prop(props, "dovetail_inplane_offset_u_mm", text='Offset along Width (mm)')
                    if _exists(props, "dovetail_inplane_offset_v_mm"):
                        s.prop(props, "dovetail_inplane_offset_v_mm", text='Offset along Length (mm)')
                    if _exists(props, "dovetail_inplane_rotation_deg"):
                        s.prop(props, "dovetail_inplane_rotation_deg", text='Rotation in plane (deg)')

            # --- Custom connector ---
            elif ctype == "CUSTOM":
                if _exists(props, "custom_connector_object"):
                    gbox.prop(props, "custom_connector_object", text='Select connector object')
                if _exists(props, "custom_connector_width_mm"):
                    gbox.prop(props, "custom_connector_width_mm", text='Custom Width (mm)')
                if _exists(props, "custom_connector_length_mm"):
                    gbox.prop(props, "custom_connector_length_mm", text='Custom Length (mm)')
                if _exists(props, "custom_connector_depth_mm"):
                    gbox.prop(props, "custom_connector_depth_mm", text='Custom Depth (mm)')
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text='Insert Depth (%)')

                # NEW: Chamfer (reuses the shared add_chamfer_mm property)
                if _exists(props, "add_chamfer_mm"):
                    gbox.prop(props, "add_chamfer_mm", text='Chamfer (mm)')

                # NEW: Span Axis / Hard-side Cut (reuses the shared dovetail_* properties)
                if _exists(props, "dovetail_span_axis"):
                    gbox.prop(props, "dovetail_span_axis", text='Span Axis')
                    if str(getattr(props, "dovetail_span_axis", "NONE")) != "NONE":
                        gbox.label(text='Forces hard-side cut along this axis.', icon='INFO')
                if _exists(props, "dovetail_hard_side_cut"):
                    gbox.prop(props, "dovetail_hard_side_cut", text='Hard-side Cut')

                # NEW: Snap Spheres — own checkbox, then the shared snap_* properties
                if _exists(props, "custom_snap_spheres_enabled"):
                    s = gbox.box()
                    s.prop(props, "custom_snap_spheres_enabled", text='Enable Snap Spheres')
                    if getattr(props, "custom_snap_spheres_enabled", False):
                        if _exists(props, "snap_spheres_per_side"):
                            s.prop(props, "snap_spheres_per_side", text='Spheres per side')
                        if _exists(props, "snap_sphere_diameter_mm"):
                            s.prop(props, "snap_sphere_diameter_mm", text='Sphere Diameter (mm)')
                        if _exists(props, "snap_sphere_protrusion_mm"):
                            s.prop(props, "snap_sphere_protrusion_mm", text='Protrusion (mm)')

                # NEW: Placement (reuses the shared dovetail_inplane_* properties)
                extra = gbox.box()
                extra.label(text='Placement', icon='ORIENTATION_GLOBAL')
                if _exists(props, "dovetail_inplane_offset_u_mm"):
                    extra.prop(props, "dovetail_inplane_offset_u_mm", text='Offset along Width (mm)')
                if _exists(props, "dovetail_inplane_offset_v_mm"):
                    extra.prop(props, "dovetail_inplane_offset_v_mm", text='Offset along Length (mm)')
                if _exists(props, "dovetail_inplane_rotation_deg"):
                    extra.prop(props, "dovetail_inplane_rotation_deg", text='Rotation in plane (deg)')

            else:
                gbox.label(text='Unsupported connector type', icon='INFO')

        layout.separator()

        # =========================
        # TOLERANCE
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text='Tolerance', icon='MOD_SOLIDIFY')
        more_txt = 'Less...' if getattr(props, "ui_more_tol", False) else 'More...'
        if _exists(props, "ui_more_tol"):
            header.prop(props, "ui_more_tol", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "material_profile"):
            col.prop(props, "material_profile", text='Material Profiles')

        if getattr(props, "ui_more_tol", False):
            adv = box.column(align=True)
            if _exists(props, "tol_override"):
                row = adv.row(align=True)
                row.prop(props, "tol_override", text='Tolerance per Face (mm)')

            # Profile numeric hint
            try:
                prof_key = getattr(props, "material_profile", None)
                prof_val = MATERIAL_PROFILES.get(prof_key, 0.2)
                row = adv.row(align=True)
                row.label(text='Profile: ' + f"{prof_val:.2f} mm")
            except Exception:
                pass

            # Effective tolerance
            try:
                if hasattr(props, "effective_tolerance") and callable(props.effective_tolerance):
                    eff_tol = float(props.effective_tolerance())
                    row2 = adv.row(align=True)
                    row2.label(text='Effective: ' + f"{eff_tol:.2f} mm")
            except Exception:
                pass

            # Short print-fit hint
            adv.label(text='For tight fit, reduce tolerance; for easy assembly, increase.', icon='INFO')

        # =========================
        # ALIGNMENT (Object Mode)
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text='Alignment', icon='SNAP_ON')

        more_txt = 'Less...' if getattr(props, "ui_more_align", False) else 'More...'
        if _exists(props, "ui_more_align"):
            header.prop(props, "ui_more_align", text=more_txt, toggle=True)

        if getattr(props, "ui_more_align", False):
            col = box.column(align=True)
            col.label(text='Pick faces in Object Mode (A = target, B = moving)')

            # Read the picks from the PropertyGroup; fall back to "nothing picked" if it is missing
            picks = getattr(context.window_manager, "snapsplit_picks", None)
            nameA = picks.face_a_obj if picks else ""
            idxA = picks.face_a_index if picks else -1
            nameB = picks.face_b_obj if picks else ""
            idxB = picks.face_b_index if picks else -1

            status_a = (f"{'A'}: {nameA} [#{idxA}]" if nameA and idxA >= 0 else 'A: none')
            status_b = (f"{'B'}: {nameB} [#{idxB}]" if nameB and idxB >= 0 else 'B: none')

            stat = box.row(align=True)
            stat.label(text=status_a, icon='INFO')
            stat.label(text=status_b, icon='INFO')
            stat.operator("snapsplit.clear_picks", text="", icon='X')

            row = box.row(align=True)
            # Invoke both face pickers in the viewport WINDOW region.
            row.operator_context = 'INVOKE_REGION_WIN'
            row.operator("snapsplit.pick_face_a", text='Pick Face A', icon='MOUSE_LMB')
            row.operator("snapsplit.pick_face_b", text='Pick Face B', icon='MOUSE_LMB')


            can_align = (bool(nameA) and idxA >= 0 and bool(nameB) and idxB >= 0)
            row_align = box.row(align=True)
            row_align.enabled = can_align
            row_align.operator("snapsplit.align_faces", text='Align Faces', icon='SNAP_ON')



def register():
    """Register panel class with Blender."""
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    """Unregister panel class from Blender."""
    bpy.utils.unregister_class(SNAP_PT_panel)

```

---

### utils.py

```py
'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''

# utils.py

import bpy
from mathutils import Vector


# ---------------------------
# Collections / objects
# ---------------------------

def ensure_collection(name):
    """Ensure a collection with the given name exists; create and link it if missing."""
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def link_to_collection(obj, coll):
    """Unlink object from its collections (safe) and link it to the target collection."""
    for c in obj.users_collection:
        try:
            c.objects.unlink(obj)
        except Exception:
            pass
    try:
        coll.objects.link(obj)
    except Exception:
        pass


def obj_world_bb(obj):
    """Return (min, max) of the object's world-space axis-aligned bounding box."""
    mat = obj.matrix_world
    coords = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(c.x for c in coords), min(c.y for c in coords), min(c.z for c in coords)))
    max_v = Vector((max(c.x for c in coords), max(c.y for c in coords), max(c.z for c in coords)))
    return min_v, max_v


# ---------------------------
# Units: keep compatibility with the working scene
# ---------------------------

def unit_mm():
    """Return the scene units per millimeter (1.0 for mm scenes, 0.001 for meter-based scenes)."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
            return 1.0
    return 0.001


def mm_to_scene(mm_value: float) -> float:
    """Convert a length in millimeters to scene units, honoring metric settings."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(mm_value)
    return float(mm_value) * 0.001


def scene_to_mm(scene_value: float) -> float:
    """Convert a length in scene units to millimeters, honoring metric settings."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(scene_value)
    return float(scene_value) / 0.001


# ---------------------------
# Modifier handling
# ---------------------------

def apply_modifier_data(obj, mod):
    """Apply ONE modifier to obj's mesh without bpy.ops.object.modifier_apply.

    The stack is evaluated with only this modifier enabled, the evaluated mesh replaces
    obj.data and the modifier is removed. Other modifiers keep their state.
    Raises RuntimeError on failure so the caller's existing try/except can report it;
    on failure the object is left as it was (the modifier stays on the stack).
    """
    if obj is None or obj.type != 'MESH' or obj.data is None:
        raise RuntimeError("apply_modifier_data: object is not a mesh")
    mod_name = mod.name
    if obj.modifiers.get(mod_name) is None:
        raise RuntimeError(f"modifier '{mod_name}' not found on '{obj.name}'")

    # Shared mesh data would change other users too: give this object its own copy
    if obj.data.users > 1:
        obj.data = obj.data.copy()

    # Evaluate with ONLY this modifier enabled; restore the other flags in any case
    saved = [(m.name, m.show_viewport) for m in obj.modifiers]
    new_mesh = None
    try:
        for m in obj.modifiers:
            m.show_viewport = (m.name == mod_name)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        new_mesh = bpy.data.meshes.new_from_object(
            obj_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
    finally:
        for name, visible in saved:
            m = obj.modifiers.get(name)
            if m is not None:
                m.show_viewport = visible

    if new_mesh is None:
        raise RuntimeError(f"modifier '{mod_name}' produced no mesh")

    # Swap the mesh, drop the modifier, keep the old data-block name
    old_mesh = obj.data
    old_name = old_mesh.name
    obj.data = new_mesh
    obj.modifiers.remove(obj.modifiers.get(mod_name))
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)
        new_mesh.name = old_name


# ---------------------------
# Localization (Blender-native)
# ---------------------------
# The English text is the lookup key. Static labels (bl_label, name=, description=,
# layout.label(text="...")) are translated by Blender itself via the dictionary that
# __init__.py registers from localization.py. The helpers below are only needed for
# strings that contain {placeholders}, because Blender cannot translate a string
# after it has been formatted.

def _translate(kind: str, msgid: str) -> str:
    """Translate 'msgid' with the pgettext variant for 'kind' ('iface' or 'rpt').

    Returns 'msgid' unchanged if translation support is missing or anything fails.
    """
    try:
        trans = bpy.app.translations
        func = trans.pgettext_rpt if kind == "rpt" else trans.pgettext_iface
        return func(msgid)
    except Exception:
        return msgid


def _format_safe(translated: str, template: str, fmt: dict) -> str:
    """Fill {placeholders} of a translated text; fall back to the English template.

    A translation with a missing or broken placeholder must never raise an error
    or show raw braces to the user.
    """
    try:
        return translated.format(**fmt)
    except (KeyError, IndexError, ValueError):
        try:
            return template.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return translated


def _trf(msgid, default=None, /, **fmt) -> str:
    """Translate an English TEMPLATE for UI text and fill its placeholders.

    New style: _trf("Created {count} parts.", count=n)
    Old style (transitional): _trf("some.key", "Created {count} parts.", count=n)
    In the old style the key is ignored and 'default' is used as the template.
    Both parameters are positional-only, so placeholders may use any name.
    """
    template = str(default if default is not None else msgid)
    return _format_safe(_translate("iface", template), template, fmt)



def tr(key, default=""):
    """DEPRECATED compatibility shim for the old key-based tr().

    Translates the English 'default' (or the key if no default is given) through
    Blender's dictionary. Remove it once no module calls tr() anymore.
    """
    return _translate("iface", default or key)


def current_language():
    """Return the active Blender UI locale like 'en_US' or 'de_DE'; 'en_US' as fallback."""
    try:
        return bpy.app.translations.locale or "en_US"
    except Exception:
        return "en_US"


def is_lang_de():
    """Return True if the current UI language starts with 'de' (German)."""
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return False


def report_user(self, level, msg, *_legacy, **fmt):
    """Report a message to the user and print it to the console.

    'msg' is an English text or an English template with {placeholders}.
    It is translated with the 'reports' variant of Blender's translation lookup.
    Placeholders are only filled when keyword arguments are given, e.g.:
        report_user(self, 'ERROR', "Modal error: {error}", error=e)

    Extra positional arguments (the removed 'msg_de' parameter) are ignored so that
    leftover old calls keep working.
    """
    template = str(msg)
    text = _translate("rpt", template)
    if fmt:
        text = _format_safe(text, template, fmt)

    if hasattr(self, "report"):
        try:
            self.report({level}, text)
        except Exception:
            pass
    print(f"[SnapSplit][{level}] {text}")


# ---------------------------
# Viewport X-Ray management (reference counted per 3D viewport)
# ---------------------------

# Maps a viewport key (SpaceView3D pointer) to its saved state:
#   {"attr": "show_xray" | "show_xray_wireframe", "saved": bool, "reasons": set of str}
# Several previews can be active at once; X-Ray is only restored when the last one ends.
_XRAY_STATES = {}


def _xray_attr_for_space(space):
    """Return the X-Ray property name valid for the viewport's shading mode, or None."""
    shading_type = space.shading.type
    if shading_type == 'SOLID':
        return "show_xray"
    if shading_type == 'WIREFRAME':
        return "show_xray_wireframe"
    # Material Preview / Rendered have no X-Ray, nothing is hidden there anyway
    return None


def _xray_find_view3d_space(context):
    """Find the 3D viewport the user is working in (context first, then the window's screen)."""
    try:
        space = getattr(context, "space_data", None)
        if space is not None and getattr(space, "type", "") == 'VIEW_3D':
            return space
    except Exception:
        pass
    try:
        area = getattr(context, "area", None)
        if area is not None and area.type == 'VIEW_3D':
            return area.spaces.active
    except Exception:
        pass
    try:
        window = getattr(context, "window", None) or bpy.context.window
        screen = getattr(window, "screen", None)
        if screen is not None:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    return area.spaces.active
    except Exception:
        pass
    return None


def _xray_space_from_key(key):
    """Find a live SpaceView3D by its pointer key; return None if it no longer exists."""
    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                for sp in area.spaces:
                    if sp.type == 'VIEW_3D' and sp.as_pointer() == key:
                        return sp
    except Exception:
        pass
    return None


def xray_acquire(context, reason):
    """Switch X-Ray on in the clicked 3D viewport and remember its previous state.

    'reason' identifies the preview that needs X-Ray (e.g. "split_preview").
    The previous state is stored once per viewport, so it is never overwritten by
    a second preview. Returns True if X-Ray is active for this reason.
    """
    try:
        space = _xray_find_view3d_space(context)
        if space is None:
            return False
        attr = _xray_attr_for_space(space)
        if attr is None:
            return False

        key = space.as_pointer()
        state = _XRAY_STATES.get(key)
        if state is not None and state["attr"] != attr:
            # Shading mode changed since the first acquire: restore the old property first
            try:
                setattr(space.shading, state["attr"], state["saved"])
            except Exception:
                pass
            state = None
        if state is None:
            state = {"attr": attr, "saved": bool(getattr(space.shading, attr)), "reasons": set()}
            _XRAY_STATES[key] = state

        state["reasons"].add(reason)
        # Set it again every time, in case it was switched off by hand in the meantime
        setattr(space.shading, attr, True)
        return True
    except Exception as ex:
        print(f"[SnapSplit] X-Ray acquire failed: {ex}")
        return False


def xray_release(reason=None):
    """Drop one reason for X-Ray; restore the saved state when no reason is left.

    reason=None drops all reasons (used on unregister). Safe to call at any time,
    it does nothing if the reason is not active.
    """
    try:
        for key in list(_XRAY_STATES.keys()):
            state = _XRAY_STATES[key]
            if reason is None:
                state["reasons"].clear()
            elif reason in state["reasons"]:
                state["reasons"].discard(reason)
            else:
                continue
            if state["reasons"]:
                continue  # another preview still needs X-Ray
            space = _xray_space_from_key(key)
            if space is not None:
                try:
                    setattr(space.shading, state["attr"], state["saved"])
                except Exception:
                    pass
            del _XRAY_STATES[key]
    except Exception as ex:
        print(f"[SnapSplit] X-Ray release failed: {ex}")



# ---------------------------
# Add-on hooks
# ---------------------------

def register():
    """Required add-on hook (no-op for utilities)."""
    pass


def unregister():
    """Required add-on hook (no-op for utilities)."""
    pass

```
